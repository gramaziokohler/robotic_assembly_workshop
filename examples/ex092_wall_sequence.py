"""Identify the sequence of blocks that needs to be placed first in order to
place a selected block.

Steps
-----
1. Load an assembly from a JSON file.
2. Select a (random) block from the top course.
3. Compute the sequence.
4. Visualise the result.

"""
import os

from math import pi
from random import choice

from compas.utilities import i_to_red

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence
from compas_assembly.datastructures import assembly_transform

from compas_assembly.plotter import AssemblyPlotter

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, '090_wall_courses.json')

# load an assembly from a JSON file

assembly = Assembly.from_json(PATH)

# get a random block from the top course

c_max = max(assembly.get_vertices_attribute('course'))

top = list(assembly.vertices_where({'course': c_max}))
key = choice(top)

# get the sequence

sequence = assembly_block_building_sequence(assembly, key)
print(sequence)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)

i_min = 0
i_max = len(sequence)
i_spn = i_max - i_min

facecolor = {k: '#cccccc' for k in assembly.vertices()}
facecolor.update({k: i_to_red((index - i_min) / i_spn) for index, k in enumerate(sequence)})
facecolor[key] = '#ff0000'

plotter.draw_blocks(facecolor=facecolor)
plotter.show()
