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

# Add the platform.stl as collision mesh to the planning scene
?


# Settings
group = "abb"

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
# Define a "good" picking configuration
picking_configuration = ?

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)


# Load assembly
assembly = Assembly.from_json(PATH_FROM)

c_max = max(assembly.get_vertices_attribute('course'))
keys_on_top = list(assembly.vertices_where({'course': c_max}))

# Iterate over the keys on top of the assembly
for key_on_top in keys_on_top:

    # Define the sequence to be build:
    # generate a building sequence from the key of the assembly
    sequence = ?
    # exclude the keys that have been already checked

    # Iterate over the assembly

        # Read the placing frame from brick, zaxis down
        o, uvw = assembly_block_placing_frame(assembly, key)
        placing_frame = Frame(o, uvw[1], uvw[0])

        # Calculate the saveframe at placing frame
        saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

        # Check ik for placing_frame and for saveframe_place
        # Only if both work, save to solutions


assembly.to_json(PATH_TO)

robot.client.close()
robot.client.terminate()
