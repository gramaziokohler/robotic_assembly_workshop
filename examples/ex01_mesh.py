import compas
from compas.datastructures import Mesh

mesh = Mesh.from_obj(compas.get('faces.obj'))

print(mesh)