"""Compute the contact forces required for static equilibrium
of a specific sequence of blocks of an assembly.

Steps
-----
1. Load an assembly from a JSON file.
2. Make a sub-assembly corresponding to the building sequence.
3. Check if the sub-assembly is properly supported.
4. Compute interface forces.
5. Serialize the result.

"""
import os

from compas_assembly.datastructures import Assembly

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'wall_sequence_equilibrium.json')

# load an assembly

assembly = Assembly.from_json(PATH)

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
