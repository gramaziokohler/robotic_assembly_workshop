from math import pi

import os

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'wall_supported.json')


assembly = Assembly.from_json(PATH)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)

supports = list(assembly.vertices_where({'is_support': True}))


plotter.draw_blocks(
    edgecolor=edgecolor,
    edgewidth=edgewidth
)
plotter.show()
