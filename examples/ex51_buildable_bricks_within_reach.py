"""
Search for buildable bricks within the robot's reach.

1. Load assembly
2. Add platform as collision mesh
3. Iterate over bricks and check ik for placing frame and saveframe
4. Save solution.
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

path = os.path.join(HERE, "robot_description")

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

# Add platform as collision mesh
package = "abb_linear_axis"
mesh = Mesh.from_stl(os.path.join(path, package, 'meshes', 'collision', 'platform.stl'))
robot.add_collision_mesh_to_planning_scene('platform', mesh)

# Load assembly
path = os.path.abspath(os.path.join(HERE, "..", "data"))
filepath = os.path.join(path, "01_wall_transformed.json")
assembly = Assembly.from_json(filepath)

# Define the sequence to be build
#key = 33 
#placed = list(assembly.vertices_where({'is_placed': True}))
#sequence = assembly_block_building_sequence(assembly, key)
#sequence = list(set(sequence) - set(placed))
sequence = [3, 2, 1, 0, 8, 7, 6, 5, 13, 12, 11, 18, 17, 16, 23, 22, 27, 28, 33]

# Settings
group = "abb"

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
picking_configuration = Configuration.from_prismatic_and_revolute_values([-1.800], [0.569, 0.849, -0.235, 6.283, 0.957, 2.140])

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

# Iterate over placing frames
for key in sequence:

    start_configuration = picking_configuration

    # Read the placing frame from brick, zaxis down
    o, uvw = assembly_block_placing_frame(assembly, key)
    placing_frame = Frame(o, uvw[1], uvw[0])

    # Calculate saveframe at placing frame
    saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

    # Check ik for placing_frame and saveframe_place
    # Only if both work, save to solutions
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
            #print(start_configuration)
            print("Brick with key %d is buildable" % key)
            assembly.blocks[key].attributes.update({'is_buildable': True})   

        except RosError as error:
            print("Brick with key %d is NOT buildable" % key, error)
    except RosError as error:
        print("Brick with key %d is NOT buildable" % key, error)

assembly.to_json(os.path.join(path, "02_wall_buildable.json"))

robot.client.close()
robot.client.terminate()


