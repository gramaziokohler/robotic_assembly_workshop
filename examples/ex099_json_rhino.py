from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import compas_rhino
from compas_assembly.datastructures import Assembly

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')

path = compas_rhino.select_file(folder=DATA, filter='JSON files (*.json)|*.json||')

assembly = Assembly.from_json(path)
assembly.draw({
    'layer': 'Assembly',
    'show.vertices': True,
    'show.interfaces': True,
    'show.forces': True,
    'show.forces_as_vectors': False,
    'mode.interface': 0,
    'scale.force': 1.0
})
