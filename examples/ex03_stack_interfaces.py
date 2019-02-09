"""Identify the interfaces of a stack.

1. Load a stack from a json file
2. Identify the interfaces
3. Export to json
4. Visualise

"""
from math import pi

import os

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.datastructures import assembly_interfaces_numpy

from compas_assembly.plotter import AssemblyPlotter

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'stack.json')

# load assembly

assembly = Assembly.from_json(PATH)

# identify_interfaces

assembly_interfaces_numpy(assembly)

# for u, v, attr in assembly.edges(data=True):
#     print(u, v)
#     print(attr)

# export to json

assembly.to_json(PATH)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0.0, 0.0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(10, 7))

plotter.draw_vertices(text={key: str(key) for key in assembly.vertices()})
plotter.draw_edges()

plotter.draw_blocks(
    facecolor={key: (255, 0, 0) for key in assembly.vertices_where({'is_support': True})}
)

plotter.show()
