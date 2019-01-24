import os
import time

from ex21_load_compas_fab_robot import robot

from compas.datastructures import Mesh

group = robot.main_group_name
brick = Mesh.from_obj(os.path.join(os.path.dirname(__file__), "brick.obj"))
robot.add_attached_collision_mesh('brick', brick, group)

time.sleep(1)
