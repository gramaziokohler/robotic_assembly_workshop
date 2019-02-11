import os

from math import pi

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, '08_wall_interfaces.json')

# load an assembly from JSON

assembly = Assembly.from_json(PATH)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6))

supports = list(assembly.vertices_where({'is_support': True}))

edgecolor = {key: '#444444' for key in assembly.vertices()}
edgecolor.update({key: '#ff0000' for key in supports})

edgewidth = {key: 0.5 for key in assembly.vertices()}
edgewidth.update({key: 3.0 for key in supports})

plotter.draw_vertices(radius=0.01)
plotter.draw_edges()
plotter.draw_blocks(edgecolor=edgecolor, edgewidth=edgewidth)
plotter.show()
