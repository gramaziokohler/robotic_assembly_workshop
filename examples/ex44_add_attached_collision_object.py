from ex21_load_compas_fab_robot import robot

import os
import time

from compas.datastructures import Mesh
from compas_fab.backends import RosClient

HERE = os.path.dirname(__file__)

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

group = robot.main_group_name
brick = Mesh.from_obj(os.path.join(HERE, "brick.obj"))

robot.add_attached_collision_mesh('brick', brick, group)
time.sleep(2)

robot.remove_attached_collision_mesh('brick', group)
time.sleep(2)
