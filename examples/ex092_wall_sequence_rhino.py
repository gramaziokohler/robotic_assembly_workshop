"""Identify the sequence of blocks that needs to be placed first in order to
place a selected block.

Steps
-----
1. Load an assembly from a JSON file.
2. Select a block of the assembly.
3. Compute the sequence.
4. Visualise the result.

"""
import os

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence

from compas_assembly.rhino import AssemblyArtist
from compas_assembly.rhino import AssemblyHelper

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, '090_wall_courses.json')

# load an assembly from a JSON file

assembly = Assembly.from_json(PATH)

# make a list of the blocks that were already placed

placed = list(assembly.vertices_where({'is_placed': True}))

# draw the assembly

artist = AssemblyArtist(assembly, layer="Assembly")

artist.clear_layer()
artist.draw_vertices()
artist.draw_blocks(show_faces=False, show_edges=True)

# draw filled in blocks for the placed ones

if placed:
    artist.draw_blocks(keys=placed, show_faces=True, show_edges=False)

# make sure Rhino redraws the view

artist.redraw()

# select a block

key = AssemblyHelper.select_vertex(assembly)

# exit if none was selected

if key is None:
    raise Exception("No block was selected.")

# get the sequence

sequence = assembly_block_building_sequence(assembly, key)
print(sequence)

# draw the blocks of the sequence

if sequence:
    keys = list(set(sequence) - set(placed))
    artist.draw_blocks(keys=keys, show_faces=True, show_edges=False)
    artist.redraw()
