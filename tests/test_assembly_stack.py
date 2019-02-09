import os
from random import choice

from compas.datastructures import mesh_transform
from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import scale_vector

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_interfaces_numpy

from compas_rbe.equilibrium import compute_interface_forces_cvx

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')

# number of blocks

N = 10

# block dimensions

W = 2.0
H = 0.5
D = 1.0

# empty assembly

assembly = Assembly()

# default block

box = Box.from_width_height_depth(W, H, D)
block = Block.from_vertices_and_faces(box.vertices, box.faces)

# make all blocks
# place each block on top of previous
# shift block randomly in XY plane

for i in range(N):
    b = block.copy()

    factor = choice([0.01, -0.01, 0.05, -0.05, 0.1, -0.1])
    axis = choice([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    vector = scale_vector(axis, factor)

    T = Translation([vector[0], vector[1], i * H])
    mesh_transform(b, T)

    assembly.add_block(b, is_support=(i == 0))

# identify_interfaces

assembly_interfaces_numpy(assembly)

# compute interface forces

compute_interface_forces_cvx(assembly, solver='CPLEX', verbose=True)
