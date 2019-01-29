"""Generate a stack of blocks.

1. Define the number of blocks and the block dimensions
2. Create an empty assembly.
3. Make a standard brick.
5. Add the blocks of the stack.
6. Serialise to json.
7. Visualise the result

"""
from math import pi
from random import choice

import compas_assembly

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import scale_vector
from compas.geometry import add_vectors

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_transform

from compas_assembly.plotter import AssemblyPlotter


# number of blocks

N = 10

# block dimensions

W = 2.0
H = 0.5
D = 1.0

# empty assembly


# default block


# make all blocks
# place each block on top of previous
# shift block randomly in XY plane


# export to json


# visualise
