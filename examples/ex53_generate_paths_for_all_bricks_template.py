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
PATH_TO = os.path.join(DATA, '03_wall_paths.json')

robot.client = RosClient()
robot.client.run()

# Settings
group = "abb"

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
# Define a "good" picking congfiguration
picking_configuration = ?

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

# Load assembly
assembly = Assembly.from_json(PATH_FROM)

# COLLISION SETTINGS ===========================================================

# Add the platform.stl as collision mesh to the planning scene
package = "abb_linear_axis"

# Remove brick_wall from planning scene

# Create attached collision object:
# From the brick.obj create an attached collision object attached to the end-effector

# tolerance vector for placing the brick at placing_frame, otherwise collision
tolerance_vector = Vector(0, 0, 0.003)

# PICKING PATH =================================================================
# Calculate cartesian path between picking frame and saveframe_pick (this will always be the same)

traj1 = response.solution
# Take last configuration of cartesian path as start configuration for kinematic path
start_configuration = ?
# Since the start configuration is only for one group, merge with full configuration
start_configuration = robot.merge_group_with_full_configuration(start_configuration, picking_configuration, group)

# PATH CALCULATION =============================================================

# Get the top keys of the assembly
c_max = max(assembly.get_vertices_attribute('course'))
keys_on_top = list(assembly.vertices_where({'course': c_max}))

# Iterate over the keys on top
for key_on_top in keys_on_top:

    # Define the sequence to be build:
    # generate a building sequence from the key of the assembly
    sequence = ?
    # exclude the keys that have been already checked

    # Iterate over the sequence

        # Read the placing frame from brick, zaxis down
        o, uvw = assembly_block_placing_frame(assembly, key)
        placing_frame = Frame(o, uvw[1], uvw[0])

        # create attached collision object
        brick = assembly.blocks[key]

        # Calculate the saveframe at placing frame
        saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

        # Calculate kinematic path *traj2* between saveframe_pick and saveframe_place with
        # attached brick collision object
        paths.append(response.solution)

        # Calculate cartesian path *traj3* between saveframe_place and placing_frame with
        # attached brick collision object
        paths.append(response.solution)

        # Update attributes
        assembly.set_vertex_attribute(key, 'is_planned', True)
        assembly.set_vertex_attribute(key, 'paths', [path.msg for path in paths])

        # Add placed brick as collision mesh to planning scene



# save assembly
assembly.to_json(PATH_TO)

robot.client.close()
robot.client.terminate()
