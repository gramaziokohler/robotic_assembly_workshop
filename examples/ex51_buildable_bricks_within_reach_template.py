"""
"""

import os
import json

from compas.geometry import Frame
from compas.geometry import Vector
from compas.datastructures import Mesh

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends import RosError

from ex50_abb_linear_axis_robot import robot

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

# Add the platform.stl as collision mesh to the planning scene

# Load the assembly from the saved json file

# Settings
group = "abb"

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
# Define a "good" picking configuration
picking_configuration = ?

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

solutions = []

# Select a top brick and generate a building sequence from the assembly
sequence = ?

# Iterate over the assembly

    # calculate the placing frame
    placing_frame = ?

    # Calculate the saveframe at placing frame
    saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

    # Check ik for placing_frame and for saveframe_place
    # Only if both work, save to solutions

# Save solutions to json file           

robot.client.close()
robot.client.terminate()


