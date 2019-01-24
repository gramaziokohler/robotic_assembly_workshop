from compas_fab.backends import RosClient

client = RosClient()
client.run()

client.on_ready(lambda: print('Is ROS connected?', client.is_connected))

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

client.terminate()
