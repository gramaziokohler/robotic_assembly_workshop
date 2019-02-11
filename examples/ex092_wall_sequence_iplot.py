"""Interactively identify the sequence of blocks that needs to be placed first
in order to place a selected block.

Steps
-----
1. Load an assembly from a JSON file.
2. Identify the blocks of the top course.
3. Set up listeners for picking events.
4. Make a plotter.
5. Visualise the assembly.
6. Add the vertices of the top course blocks as pickable handles.
7. Compute the required sequence of blocks when a block of the top course is selected.

"""
import os

from math import pi

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

# get the blocks of the top course

c_max = max(assembly.get_vertices_attribute('course'))
top = list(assembly.vertices_where({'course': c_max}))

# make a index -> key map

index_key = {index: key for index, key in enumerate(top)}


# listners

def compute_sequence(key):
    placed = set(assembly.vertices_where({'is_placed': True}))

    if key in placed:
        return

    sequence = assembly_block_building_sequence(assembly, key)
    sequence[:] = [key for key in sequence if key not in placed]

    assembly.set_vertices_attribute('is_placed', True, keys=sequence)

    i_min = 0
    i_max = len(sequence)
    i_spn = i_max - i_min

    facecolor = {key: '#eeeeee' for key in assembly.vertices()}

    facecolor.update({key: '#cccccc' for key in placed})
    facecolor.update({key: i_to_red((index - i_min) / i_spn) for index, key in enumerate(sequence)})

    facecolor[key] = '#ff0000'

    plotter.clear_blocks()
    plotter.draw_blocks(facecolor=facecolor)


def on_pick(e):
    index = e.ind[0]
    key = index_key[index]
    if key in top:
        compute_sequence(key)
        plotter.update()


# interactive visualisation

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)

plotter.draw_blocks(facecolor={k: '#eeeeee' for k in assembly.vertices()})
plotter.draw_vertices(keys=top, radius=0.01, picker=10)
plotter.register_listener(on_pick)
plotter.show()
