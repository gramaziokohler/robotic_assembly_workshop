"""
Example to calculate collision free paths for a brick wall.
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

from ex50_abb_linear_axis_robot import robot

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

# Add the platform.stl as collision mesh to the planning scene

# Remove brick_wall from planning scene

# From the brick.obj create an attached collision object attached to the end-effector

# Load the assembly from the saved json file

# Settings
group = "abb"

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
# Define a "good" picking congfiguration
picking_configuration = ?

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

# Optional: constrain movement of one or several axes 
path_constraints = ?

solutions = []

# Select a top brick and generate a building sequence from the assembly
sequence = ?


# Calculate cartesian path between picking frame and saveframe_pick


# Take last configuration of cartesian path as start configuration for kinematic path
start_configuration = ?
# Since the start configuration is only for one group, merge with full configuration
start_configuration = robot.merge_group_with_full_configuration(start_configuration, picking_configuration, group)


# Iterate over sequence

    # calculate the placing frame
    placing_frame = ?

    # Calculate the saveframe at placing frame
    saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

    # Calculate kinematic path between saveframe_pick and saveframe_place and
    # attach the brick collision object

    # Calculate cartesian path between saveframe_place and placing_frame
    

    # Add placed brick as collision mesh to planning scene


# Save solutions to json.

robot.client.close()
robot.client.terminate()


