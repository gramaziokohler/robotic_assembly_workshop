"""Identify the courses of a assembly assembly.

Steps
-----
1. Load an assembly from a JSON file.
2. Identify the course rows
3. serialise to JSON

Notes
-----
This will only work as expected on *wall* assemblies that are properly supported.

Exercise
--------
Check if all blocks of bottom course are supported.

"""
import os

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_courses

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH_FROM = os.path.join(DATA, 'wall_interfaces.json')
PATH_TO = os.path.join(DATA, 'wall_courses.json')

# load an assembly from JSON

assembly = Assembly.from_json(PATH_FROM)

# check if the assembly has supports

supports = list(assembly.vertices_where({'is_support': True}))

if not supports:
    raise Exception("The assembly has no supports.")

# identify the courses

courses = assembly_courses(assembly)

# assign course id's to the corresponding blocks

for i, course in enumerate(courses):
    assembly.set_vertices_attribute('course', i, keys=course)

# serialise the result

assembly.to_json(PATH_TO)
