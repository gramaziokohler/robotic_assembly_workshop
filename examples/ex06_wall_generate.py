"""Generate an assembly describing a brick wall.

Steps
-----
1. Create brick geometry
2. Create half brick geometry
3. Make an empty assembly
4. Add bricks in staggered pattern
5. Serialise the result

Parameters
----------
number_of_even_bricks : int
    The number of bricks on the even rows.
number_of_courses : int
    The number of course rows in the wall.
width : float
    The width of the base brick.
height : float
    The height of the base brick.
depth : float
    The depth of the base brick.
gap : float
    The horizontal gap between the bricks.

Warning
-------
Don't go crazy with the number of bricks.
The CPLEX community edition of the solver only allows for 1000 variables,
and you reach that number really quickly...

Exercise
--------
Mark courses of bricks already during the wall generation process.

"""
import os

from compas.geometry import Box
from compas.geometry import Translation

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, '06_wall.json')

# number of bricks in even courses

number_of_even_bricks = 5

# number of courses

number_of_courses = 7

# brick dimensions

width = 0.240
height = 0.052
depth = 0.116

# horizontal joints

gap = 0.02

# brick geometry

box = Box.from_width_height_depth(width, height, depth)
brick = Block.from_vertices_and_faces(box.vertices, box.faces)

# halfbrick geometry

box = Box.from_width_height_depth(0.5 * (width - gap), height, depth)
halfbrick = Block.from_vertices_and_faces(box.vertices, box.faces)

# empty assembly

assembly = Assembly()

# add bricks in a staggered pattern

for i in range(number_of_courses):
    dy = i * height

    if i % 2 == 0:
        # in the even rows
        # add (number_of_even_bricks) full bricks

        for j in range(number_of_even_bricks):
            block = brick.copy()
            mesh_transform(block, Translation([j * (width + gap), 0, dy]))
            assembly.add_block(block)
    else:
        # in the uneven rows
        # add a half brick
        # add (number_of_even_bricks - 1) full bricks
        # add a half brick

        block = halfbrick.copy()
        mesh_transform(block, Translation([0, 0, dy]))
        assembly.add_block(block)

        for j in range(number_of_even_bricks - 1):
            block = brick.copy()
            mesh_transform(block, Translation([(0.5 + j) * (width + gap), 0, dy]))
            assembly.add_block(block)

        block = halfbrick.copy()
        mesh_transform(block, Translation([(0.5 + j + 1) * (width + gap), 0, dy]))
        assembly.add_block(block)

# export to json

assembly.to_json(PATH)
