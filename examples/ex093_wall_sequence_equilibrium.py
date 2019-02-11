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

from compas_rbe.equilibrium import compute_interface_forces_cvx

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH_FROM = os.path.join(DATA, 'wall_courses.json')
PATH_TO = os.path.join(DATA, 'wall_sequence_equilibrium.json')

# load an assembly

assembly = Assembly.from_json(PATH_FROM)

# define a sequence of buildable blocks

sequence = [28, 22, 23, 16, 17, 18, 11, 12, 13, 5, 6, 7, 8, 0, 1, 2, 3, 38]

# create a sub_assembly for the sequence

sub = assembly.subset(sequence)

# check if the sub_assembly is supported

supports = list(sub.vertices_where({'is_support': True}))

if not supports:
    raise Exception('The sub-assembly has no supports.')

# compute the interface forces

compute_interface_forces_cvx(sub, solver='CPLEX', verbose=True)

# update the original assembly

for u, v, attr in assembly.edges(True):
    if sub.has_edge(u, v):
        attr['interface_forces'] = sub.get_edge_attribute((u, v), 'interface_forces')
    else:
        attr['interface_forces'] = None

# serialise to json

assembly.to_json(PATH_TO)
