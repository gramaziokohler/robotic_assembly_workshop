"""Generate an assembly describing a brick wall.

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

Notes
-----
The script below does the same as ``compas_assembly.datastructures.assembly_construct_wall()``.

"""
import compas_assembly

from compas.geometry import Box
from compas.geometry import Translation

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block


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


# halfbrick geometry


# empty assembly


# add bricks in a staggered pattern

for i in range(number_of_courses):
    dy = i * height

    if i % 2 == 0:
        # in the even rows
        # add (number_of_even_bricks) full bricks


    else:
        # in the uneven rows
        # add a half brick
        # add (number_of_even_bricks - 1) full bricks
        # add a half brick


# export to json

