from ex22_load_compas_fab_robot import robot

import os
import time

from compas.datastructures import Mesh
from compas_fab.backends import RosClient

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'floor.stl')

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

floor = Mesh.from_stl(PATH)
robot.add_collision_mesh_to_planning_scene("floor", floor)
# robot.remove_collision_mesh_from_planning_scene("floor")

time.sleep(1)
