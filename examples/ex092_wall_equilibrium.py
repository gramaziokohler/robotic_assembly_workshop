"""Compute the contact forces required for static equilibrium of an assembly.

1. Make an Xfunc of ``compute_interface_forces``
2. Load an assembly from a JSON file.
3. Make a sub-assembly corresponding to the building sequence.
4. Check if the sub-assembly is properly supported.
5. Compute interface forces.
6. Visualise in Rhino.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import compas

from compas_rhino.utilities import XFunc
from compas_assembly.datastructures import Assembly

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'wall_courses.json')

# make an XFunc version of the compute interfaces function


# path to CPython on RhinoMac
# change this if necessary

if compas.is_mono():
    python = os.path.join(os.environ['HOME'], 'anaconda3/bin/python')
    compute_interface_forces_xfunc.python = python

# a convenience wrapper

def compute_interface_forces(assembly, **kwargs):
    data = {
        'assembly': assembly.to_data(),
        'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
    }
    result = compute_interface_forces_xfunc(data, **kwargs)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]

# load an assembly from a JSON file

assembly = Assembly.from_json(PATH)

# define a sequence of buildable blocks


# create a sub_assembly for the sequence


# check if the sub_assembly is supported


# compute the interface forces


# update the original assembly


# visualise the result

assembly.draw({
    'layer': 'Assembly',
    'show.vertices': True,
    'show.interfaces': True,
    'show.forces': True,
    'show.forces_as_vectors': False,
    'mode.interface': 0,
    'scale.force': 1.0
})
