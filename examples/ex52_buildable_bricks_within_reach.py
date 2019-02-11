"""
Search for buildable bricks within the robot's reach.

1. Add platform as collision mesh
2. Load assembly from '51_wall_transformed.json'
3. Generate building sequence from assembly by a defined key.
4. Iterate over sequence and check inverse kinematic for placing_frame and
   saveframe_place
5. If solution is found for both, add {'is_buildable': True} as attribute to
   the assembly.
4. Save the assembly as '52_wall_buildable.json'.
"""

import os
import json

from compas.geometry import Frame
from compas.geometry import Vector
from compas.datastructures import Mesh

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends import RosError

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence
from compas_assembly.datastructures import assembly_block_placing_frame

from ex50_abb_linear_axis_robot import robot

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH_FROM = os.path.join(DATA, '51_wall_transformed.json')
PATH_TO = os.path.join(DATA, '52_wall_buildable.json')

robot.client = RosClient()
robot.client.run()

# Add platform as collision mesh
package = "abb_linear_axis"
mesh = Mesh.from_stl(os.path.join(DATA, 'robot_description', package, 'meshes', 'collision', 'platform.stl'))
robot.add_collision_mesh_to_planning_scene('platform', mesh)

# Settings
group = "abb"

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
picking_configuration = Configuration.from_prismatic_and_revolute_values([-1.800], [0.569, 0.849, -0.235, 6.283, 0.957, 2.140])

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

# Load assembly
assembly = Assembly.from_json(PATH_FROM)

c_max = max(assembly.get_vertices_attribute('course'))
keys_on_top = list(assembly.vertices_where({'course': c_max}))

for key_on_top in keys_on_top:

    # Define the sequence to be checked if buildable
    sequence = assembly_block_building_sequence(assembly, key_on_top)
    # exclude all that are already checked
    exclude_keys = [vkey for vkey, attr in assembly.vertices_where_predicate(lambda key, attr: \
                    attr['is_support'] or \
                    attr['is_built'] or \
                    attr['is_planned'] or \
                    attr['is_buildable'], True)]
    sequence = [k for k in sequence if k not in exclude_keys] # keep order
    print("sequence", sequence)

    # Iterate over the assembly
    for key in sequence:

        start_configuration = picking_configuration

        # Read the placing frame from brick, zaxis down
        o, uvw = assembly_block_placing_frame(assembly, key)
        placing_frame = Frame(o, uvw[1], uvw[0])

        # Calculate saveframe at placing frame
        saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

        # Check ik for placing_frame and saveframe_place
        # Only if both work, save to assembly
        try:
            response = robot.inverse_kinematics(frame_WCF=saveframe_place,
                                                start_configuration=start_configuration,
                                                group=group,
                                                constraints=None,
                                                attempts=20)
            start_configuration = response.configuration
            try:
                response = robot.inverse_kinematics(frame_WCF=placing_frame,
                                                    start_configuration=start_configuration,
                                                    group=group,
                                                    constraints=None,
                                                    attempts=20)
                start_configuration = response.configuration
                print("Brick with key %d is buildable" % key)
                assembly.set_vertex_attribute(key, 'is_buildable', True)

            except RosError as error:
                print("Brick with key %d is NOT buildable" % key, error)
        except RosError as error:
            print("Brick with key %d is NOT buildable" % key, error)

assembly.to_json(PATH_TO)

robot.client.close()
robot.client.terminate()
