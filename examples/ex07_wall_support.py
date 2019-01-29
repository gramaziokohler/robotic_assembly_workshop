"""Add a support plate to a wll assembly and identify the interfaces.

1. Load an assembly from a json file
2. Compute the footprint of the assembly
3. Add a support in the XY plane at least the size to the footprint
4. Compute the interfaces of the assembly
5. Serialise the result

"""
import compas_assembly

from compas.geometry import bounding_box_xy
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas.geometry import centroid_points

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block


# load assembly from JSON


# list the coordinates of all vertices of all blocks


# compute the XY bounding box of all listed vertices


# make a support block of the same size as the bounding box


# scale the support


# align the centroid of the support with the centroid of the bounding box


# add the support to the assembly


# serialise

