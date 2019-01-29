from math import pi

import compas_assembly

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter


assembly = Assembly.from_json(compas_assembly.get('wall_interfaces.json'))

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)

supports = list(assembly.vertices_where({'is_support': True}))

edgecolor = {key: '#444444' for key in assembly.vertices()}
edgecolor.update({key: '#ff0000' for key in supports})

edgewidth = {key: 0.5 for key in assembly.vertices()}
edgewidth.update({key: 3.0 for key in supports})

plotter.draw_blocks(
    edgecolor=edgecolor,
    edgewidth=edgewidth
)
plotter.show()
