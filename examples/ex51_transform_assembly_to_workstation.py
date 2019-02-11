"""
Move the assembly to the workstation and write assembly to json.
"""
import os

from compas.geometry import Frame
from compas.geometry import Transformation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH_FROM = os.path.join(DATA, '090_wall_courses.json')
PATH_TO = os.path.join(DATA, '51_wall_transformed.json')

assembly = Assembly.from_json(PATH_FROM)

# Set default attributes which will be changed later on in the planning process
assembly.update_default_vertex_attributes(is_buildable=False, is_planned=False, is_built=False)

# Define the frame where you want to transform the brick wall to.
pt = (-0.189775, -0.871978, 0.518383)
frame = Frame(pt, (1, 0, 0), (0, 1, 0))
T = Transformation.from_frame(frame)

# Transform the assembly
assembly_transform(assembly, T)
# serialise
assembly.to_json(PATH_TO)
