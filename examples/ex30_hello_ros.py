from compas_fab.backends import RosClient

client = RosClient()


def hello_ros():
    print('Connected: %s' % client.is_connected)
    client.terminate()


client.on_ready(hello_ros)
client.run_forever()
