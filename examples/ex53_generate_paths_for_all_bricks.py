"""
Generate paths for brick building sequence.

1. Add platform as collision mesh
2. Load assembly from '52_wall_buildable.json'
3. Check cartesian path *traj1* between picking_frame and saveframe_pick
4. Iterate over top brick keys:
5.   Generate sequence from key and iterate over assembly sequence
6.     Calulate placing_frame and saveframe_place
7.     Calculate kinematic path *traj2* between last configuration of *traj1* and frame
       saveframe_place by adding the brick as attached collision object.
8.     Calculate cartesian path *traj3* between last configuarion of *traj2* and
       placing_frame by adding the brick as attached collision object.
9.     Add newly placed brick as collision object "brick_wall" to planning scence.
10.    If solution is found for all 3 paths, add {'paths': [traj1, traj2, traj3]} as
       attribute to the brick of the assembly.
11. Save assembly into '03_wall_paths.json'
"""

import os
import json
import math
import time

from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import Transformation
from compas.datastructures import Mesh
from compas.datastructures import mesh_transformed

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends import RosError

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence
from compas_assembly.datastructures import assembly_block_placing_frame

from ex50_abb_linear_axis_robot import robot

# SETTINGS =====================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH_FROM = os.path.join(DATA, '52_wall_buildable.json')
PATH_TO = os.path.join(DATA, '53_wall_paths.json')

robot.client = RosClient()
robot.client.run()

group = "abb"
#group = "axis_abb" # Try with this as well...

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
picking_configuration = Configuration.from_prismatic_and_revolute_values([-1.800], [0.569, 0.849, -0.235, 6.283, 0.957, 2.140])

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

# Load assembly
assembly = Assembly.from_json(PATH_FROM)

# COLLISION SETTINGS ===========================================================

# Add platform as collision mesh
package = "abb_linear_axis"
mesh = Mesh.from_stl(os.path.join(DATA, 'robot_description', package, 'meshes', 'collision', 'platform.stl'))
robot.add_collision_mesh_to_planning_scene('platform', mesh)

# Remove brick_wall from planning scene
robot.remove_collision_mesh_from_planning_scene("brick_wall")

# Create attached collision object
brick = Mesh.from_obj(os.path.join(DATA, "brick.obj"))
aco = robot.create_collision_mesh_attached_to_end_effector('brick', brick, group)

# tolerance vector for placing the brick at placing_frame, otherwise collision
tolerance_vector = Vector(0, 0, 0.003)

# PICKING PATH =================================================================

# Calculate cartesian path between picking frame and saveframe_pick
response = robot.compute_cartesian_path(frames_WCF=[picking_frame, saveframe_pick],
                                        start_configuration=picking_configuration,
                                        max_step=0.01,
                                        avoid_collisions=True,
                                        group=group,
                                        path_constraints=None)
if response.fraction != 1.:
    print(response.fraction)
    raise Exception("Please check, something's wrong with picking configuration and frame...")

traj1 = response.solution

picking_configurations = response.configurations
# Take last configuration of cartesian path as start configuration for kinematic path
start_configuration = picking_configurations[-1]
# Since the start configuration is only for one group, merge with full configuration
start_configuration = robot.merge_group_with_full_configuration(start_configuration, picking_configuration, group)

# PATH CALCULATION =============================================================

# Get the top keys of the assembly
c_max = max(assembly.get_vertices_attribute('course'))
keys_on_top = list(assembly.vertices_where({'course': c_max}))

# Iterate over keys on top
for key_on_top in keys_on_top:

    # Define the sequence to be checked if buildable
    sequence = assembly_block_building_sequence(assembly, key_on_top)
    # exclude all that are already checked
    exclude_keys = [vkey for vkey, attr in assembly.vertices_where_predicate(lambda key, attr:
                    attr['is_support'] or
                    attr['is_built'] or
                    attr['is_planned'], True)]
    sequence = [k for k in sequence if k not in exclude_keys] # keep order
    print("sequence", sequence)

    # Iterate over the sequence
    for key in sequence:

        start_configuration = picking_configuration

        # Read the placing frame from brick, zaxis down
        o, uvw = assembly_block_placing_frame(assembly, key)
        placing_frame = Frame(o, uvw[1], uvw[0])

        # create attached collision object
        brick = assembly.blocks[key]
        brick_tcp = mesh_transformed(brick, Transformation.from_frame_to_frame(placing_frame, Frame.worldXY()))
        aco = robot.create_collision_mesh_attached_to_end_effector('brick', brick_tcp, group)

        saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)
        paths = [traj1]

        # Calculate kinematic path between saveframe_pick and saveframe_place
        try:
            response = robot.motion_plan_goal_frame(frame_WCF=saveframe_place,
                                                    start_configuration=start_configuration,
                                                    tolerance_position=0.005,
                                                    tolerance_angle=math.radians(1),
                                                    group=group,
                                                    path_constraints=None,
                                                    planner_id='RRT',
                                                    num_planning_attempts=20,
                                                    allowed_planning_time=8.,
                                                    attached_collision_object=aco)
            paths.append(response.trajectory)
            last_configuration = response.configurations[-1]
            last_configuration = robot.merge_group_with_full_configuration(last_configuration, picking_configuration, group)

        except RosError as error:
            print(error)
            break

        print("last_configuration", last_configuration)

        # Calculate cartesian path between saveframe_place and placing_frame
        placing_frame_tolerance = placing_frame.copy()
        placing_frame_tolerance.point += tolerance_vector

        frames = [saveframe_place, placing_frame_tolerance]
        try:
            response = robot.compute_cartesian_path(frames_WCF=frames,
                                                    start_configuration=last_configuration,
                                                    max_step=0.01,
                                                    avoid_collisions=True,
                                                    group=group,
                                                    path_constraints=None,
                                                    attached_collision_object=aco)
            if response.fraction == 1.:
                paths.append(response.solution)
                last_configuration = response.configurations[-1]
            else:
                print("Cartesian computed only %d percent of the path" % (response.fraction * 100))
                break
        except RosError as error:
            print("Cartesian:", error)
            break

        # Update attributes
        assembly.set_vertex_attribute(key, 'is_planned', True)
        assembly.set_vertex_attribute(key, 'paths', [path.msg for path in paths])
    
        # Add placed brick to planning scene
        brick_transformed = mesh_transformed(brick, Transformation.from_frame(placing_frame))
        robot.append_collision_mesh_to_planning_scene('brick_wall', brick)
    
assembly.to_json(PATH_TO)

robot.client.close()
robot.client.terminate()
