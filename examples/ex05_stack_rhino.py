from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_assembly.datastructures import Assembly

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'stack.json')

assembly = Assembly.from_json(PATH)
assembly.draw({
    'layer': 'Assembly',
    'show.vertices': True,
    'show.edges': True,
    'show.forces': True,
    'show.selfweight': True
})
