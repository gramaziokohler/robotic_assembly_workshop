"""Compute the contact forces at the interfaces between the blocks
that are required for static equilibrium of the assembly.

Warning
-------
This will not work, since the number of variables is 1040,
and the community edition of CPLEX only allows for 1000 variables and constraints.

"""
import os

from compas_assembly.datastructures import Assembly

from compas_rbe.equilibrium import compute_interface_forces_cvx

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH_FROM = os.path.join(DATA, '090_wall_courses.json')
PATH_TO = os.path.join(DATA, '091_wall_equilibrium.json')

# load an assembly from a JSON file

assembly = Assembly.from_json(PATH_FROM)

# check the supports

supports = list(assembly.vertices_where({'is_support': True}))

if not supports:
    raise Exception('The assembly has no supports.')

# compute the interface forces

compute_interface_forces_cvx(assembly, solver='CPLEX', verbose=True)

# serialise to json

assembly.to_json(PATH_TO)
