from compas.datastructures import Mesh

from compas_ghpython.artists import MeshArtist
# from compas_rhino.artists import MeshArtist
# from compas_blender.artists import MeshArtist

mesh = Mesh.from_obj('https://u.nu/hypar')

artist = MeshArtist(mesh)

artist.draw()
