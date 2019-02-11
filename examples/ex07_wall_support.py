"""Add a support plate to a wll assembly and identify the interfaces.

Steps
-----
1. Load an assembly from a json file
2. Compute the footprint of the assembly
3. Add a support in the XY plane at least the size to the footprint
4. Mark the support as *placed*.
5. Serialise the result

Parameters
----------
PADDING : float
    The padding around the footprint of the wall.

Exercise
--------
If brick courses were already assigned during the wall generation process,
add a support per block of the bottom course to simplify interface detection
afterwards.

"""
import os

from compas.geometry import bounding_box_xy
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas.geometry import centroid_points

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH_FROM = os.path.join(DATA, 'wall.json')
PATH_TO = os.path.join(DATA, 'wall_supported.json')

# parameters

PADDING = 0.1

# load assembly from JSON

assembly = Assembly.from_json(PATH_FROM)

# list the coordinates of all vertices of all blocks

points = []
for key in assembly.vertices():
    block = assembly.blocks[key]
    xyz = block.get_vertices_attributes('xyz')
    points.extend(xyz)

# compute the XY bounding box of all listed vertices

bbox = bounding_box_xy(points)

# make a support block of the same size as the bounding box

support = Block.from_vertices_and_faces(bbox, [[0, 1, 2, 3]])

# scale the support according to the padding

lx = length_vector(subtract_vectors(bbox[1], bbox[0]))
ly = length_vector(subtract_vectors(bbox[2], bbox[1]))
sx = (PADDING + lx) / lx
sy = (PADDING + ly) / ly

S = Scale([sx, sy, 1.0])

mesh_transform(support, S)

# align the centroid of the support with the centroid of the bounding box

b = centroid_points(bbox)
a = support.centroid()

mesh_transform(support, Translation(subtract_vectors(b, a)))

# add the support to the assembly
# and mark it as placed

assembly.add_block(support, is_support=True, is_placed=True)

# serialise

assembly.to_json(PATH_TO)
