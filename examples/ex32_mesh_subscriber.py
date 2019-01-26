# Copy & Paste this exercise into a Grasshopper component
# And add a `subscribe` input connected to a button

import Rhino
import scriptcontext as sc

import roslibpy

from compas_fab.backends import RosClient
from compas_fab.backends.ros.messages.shape_msgs import Mesh
from compas_ghpython.artists import MeshArtist

if subscribe:
    def receive_mesh(message):
        mesh_message = Mesh.from_msg(message)
        artist = MeshArtist(mesh_message.mesh)
        sc.doc = Rhino.RhinoDoc.ActiveDoc
        sc.doc.Objects.AddMesh(artist.draw())
        sc.doc = ghdoc

    client = RosClient()
    client.run()
    topic = roslibpy.Topic(client, '/meshes', 'shape_msgs/Mesh')
    topic.subscribe(receive_mesh)
