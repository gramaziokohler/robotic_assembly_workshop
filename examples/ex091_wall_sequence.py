""""""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence

from compas_assembly.rhino import AssemblyArtist
from compas_assembly.rhino import AssemblyHelper


# just so Rhino(Mac) gets the filepaths right

HERE = os.path.dirname(__file__)

# load an assembly from a JSON file

assembly = Assembly.from_json(os.path.join(HERE, '../data/wall_courses.json'))

# make a list of the blocks that were already placed


# draw the assembly


# draw filled in blocks for the placed ones


# make sure Rhino redraws the view


# select a block


# exit if none was selected


# get the sequence


# draw the blocks of the sequence

