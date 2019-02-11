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

robot.client = RosClient()
robot.client.run()

# Add the platform.stl as collision mesh to the planning scene

# Remove brick_wall from planning scene

# From the brick.obj create an attached collision object attached to the end-effector

# Load assembly
assembly = Assembly.from_json(PATH_FROM)

# Settings
group = "abb"

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
# Define a "good" picking congfiguration
picking_configuration = ?

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

# Optional: constrain movement of one or several axes
path_constraints = ?

# Define the sequence to be build:
# Select a top brick and generate a building sequence from the assembly
sequence = ?

# Calculate cartesian path between picking frame and saveframe_pick (this will always be the same)


# Take last configuration of cartesian path as start configuration for kinematic path
start_configuration = ?
# Since the start configuration is only for one group, merge with full configuration
start_configuration = robot.merge_group_with_full_configuration(start_configuration, picking_configuration, group)


# Iterate over sequence

    # Read the placing frame from brick, zaxis down
    o, uvw = assembly_block_placing_frame(assembly, key)
    placing_frame = Frame(o, uvw[1], uvw[0])

    # create attached collision object

    # Calculate the saveframe at placing frame
    saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

    # Calculate kinematic path between saveframe_pick and saveframe_place with
    # attached brick collision object

    # Calculate cartesian path between saveframe_place and placing_frame with
    # attached brick collision object


    # Add placed brick as collision mesh to planning scene

# save assembly
assembly.to_json(PATH_TO)

robot.client.close()
robot.client.terminate()
