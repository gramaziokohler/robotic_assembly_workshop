from ex20_load_compas_fab_robot import robot

from compas.datastructures import Mesh
from compas_fab.backends import RosClient
from compas_rhino.helpers import mesh_from_guid

client = RosClient('127.0.0.1', 9090)
robot.client = client

compas_mesh = mesh_from_guid(Mesh, mesh)
robot.add_collision_mesh_to_planning_scene("floor", compas_mesh)

client.call_later(3, client.close)
client.call_later(5, client.terminate)
client.run_forever()
