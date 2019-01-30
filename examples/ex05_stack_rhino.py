from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_assembly.datastructures import Assembly

HERE = os.path.dirname(__file__)
path = os.path.join(HERE, '../data/stack.json')

assembly = Assembly.from_json(path)
assembly.draw({
    'layer': 'Assembly',
    'show.vertices': True,
    'show.edges': True,
    'show.forces': True,
    'show.selfweight': True
})
