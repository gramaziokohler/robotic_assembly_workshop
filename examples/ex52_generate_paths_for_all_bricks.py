"""
Generate paths for brick building sequence.

1. Add platform as collision mesh
2. Load assembly from '02_wall_buildable.json'
3. Generate building sequence from assembly through the defined key.
4. Check cartesian path *p1* between picking_frame and saveframe_pick
5. Iterate over assembly sequence
6.   Calulate placing_frame and saveframe_place
7.   Calculate kinematic path *p2* between last configuration of *p1* and frame
     saveframe_place by adding the brick as attached collision object.
8.   Calculate cartesian path *p3* between last configuarion of *p2* and 
     placing_frame by adding the brick as attached collision object.
9.   Add newly placed brick as collision object "brick_wall" to planning scence.
10.  If solution is found for all 3 paths, add {'paths': [p1, p2, p3]} as 
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
from compas_fab.backends.ros import Constraints
from compas_fab.backends.ros import JointConstraint

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence
from compas_assembly.datastructures import assembly_block_placing_frame

from ex50_abb_linear_axis_robot import robot

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH_FROM = os.path.join(DATA, '02_wall_buildable.json')
PATH_TO = os.path.join(DATA, '03_wall_paths.json')

path = os.path.join(HERE, "robot_description")

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

# Add platform as collision mesh
package = "abb_linear_axis"

#group = "axis_abb"
group = "abb"

# tolerance vector for placing the brick at placing_frame, otherwise collision
tolerance_vector = Vector(0, 0, 0.003)

# Add platform as collision mesh
mesh = Mesh.from_stl(os.path.join(DATA, 'robot_description', package, 'meshes', 'collision', 'platform.stl'))
robot.add_collision_mesh_to_planning_scene('platform', mesh)

# Remove brick_wall from planning scene
robot.remove_collision_mesh_from_planning_scene("brick_wall")

# Create attached collision object
brick = Mesh.from_obj(os.path.join(DATA, "brick.obj"))
aco = robot.create_collision_mesh_attached_to_end_effector('brick', brick, group)

# Load assembly
assembly = Assembly.from_json(PATH_FROM)

# Define the sequence to be build
#key = 33 
#placed = list(assembly.vertices_where({'is_placed': True}))
#sequence = assembly_block_building_sequence(assembly, key)
#sequence = list(set(sequence) - set(placed))
sequence = [3, 2, 1, 0, 8, 7, 6, 5, 13, 12, 11, 18, 17, 16, 23, 22, 27, 28, 33]

# Settings
picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
picking_configuration = Configuration.from_prismatic_and_revolute_values([-1.800], [0.569, 0.849, -0.235, 6.283, 0.957, 2.140])

# Constrain movement of one or several axes 
pc = Constraints()
pc.joint_constraints.append(JointConstraint('joint_2', picking_configuration.values[2], math.pi/2, math.pi/2, 1.))
#pc.joint_constraints.append(JointConstraint('joint_6', picking_configuration.values[6], math.pi/2, math.pi/2, 1.))

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

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

start_trajectory = response.solution

picking_configurations = response.configurations
# Take last configuration of cartesian path as start configuration for kinematic path
start_configuration = picking_configurations[-1]
# Since the start configuration is only for one group, merge with full configuration
start_configuration = robot.merge_group_with_full_configuration(start_configuration, picking_configuration, group)

# Iterate over placing frames
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
    paths = [start_trajectory]

    # Calculate kinematic path between saveframe_pick and saveframe_place
    try:
        response = robot.motion_plan_goal_frame(frame_WCF=saveframe_place, 
                                                start_configuration=start_configuration, 
                                                tolerance_position=0.005, 
                                                tolerance_angle=math.radians(1), 
                                                group=group,
                                                path_constraints=pc, 
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
                                                path_constraints=pc,
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
    
    assembly.blocks[key].attributes.update({'paths': [path.msg for path in paths]})  

    # Add placed brick to planning scene
    brick_transformed = mesh_transformed(brick, Transformation.from_frame(placing_frame))
    robot.append_collision_mesh_to_planning_scene('brick_wall', brick)

assembly.to_json(PATH_TO)

robot.client.close()
robot.client.terminate()
