import os

from math import pi

from compas.utilities import i_to_red

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, '090_wall_courses.json')

# load an assembly from JSON

assembly = Assembly.from_json(PATH)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6))

courses = assembly.get_vertices_attribute('course')

c_min = min(courses)
c_max = max(courses)
c_spn = c_max - c_min

facecolor = {key: i_to_red((attr['course'] - c_min) / c_spn) for key, attr in assembly.vertices(True)}
edgecolor = {key: '#000000' for key in assembly.vertices_where({'is_support': True})}
edgewidth = {key: 3 for key in assembly.vertices_where({'is_support': True})}

plotter.draw_blocks(
    facecolor=facecolor,
    edgecolor=edgecolor,
    edgewidth=edgewidth
)
plotter.show()
