"""Compute the contact forces required for static equilibrium of an assembly.

1. Load an assembly from a JSON file.
2. Make sure there are supports.
3. Identify the interfaces.
4. Compute interface forces.
5. Serialise the result.

"""
from math import pi

import os

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_rbe.equilibrium import compute_interface_forces_cvx

from compas_assembly.plotter import AssemblyPlotter

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'stack.json')

# load assembly

assembly = Assembly.from_json(PATH)

# compute interface forces

compute_interface_forces_cvx(assembly, solver='CPLEX', verbose=True)

# serialise

assembly.to_json(PATH)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0.0, 0.0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(10, 7))

plotter.draw_vertices(text={key: str(key) for key in assembly.vertices()})
plotter.draw_edges()

plotter.draw_blocks(
    facecolor={key: (255, 0, 0) for key in assembly.vertices_where({'is_support': True})}
)

plotter.show()
