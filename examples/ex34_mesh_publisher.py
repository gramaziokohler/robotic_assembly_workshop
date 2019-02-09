# Copy & Paste this exercise into a Grasshopper component
# And add two inputs: `mesh` and `publish`. The first is a mesh
# of your choice, the second is a button to trigger publishing.

import time
import compas
import roslibpy

from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas_rhino.helpers import mesh_from_guid
from compas_fab.backends import RosClient
from compas_fab.backends.ros.messages import shape_msgs

compas_mesh = mesh_from_guid(Mesh, mesh)
mesh_quads_to_triangles(compas_mesh)
message = shape_msgs.Mesh.from_mesh(compas_mesh)

if publish:
    client = RosClient()
    client.run()

    topic = roslibpy.Topic(client, '/meshes', 'shape_msgs/Mesh')
    topic.advertise()
    time.sleep(1)
    topic.publish(message.msg)
    time.sleep(1)

    client.terminate()
