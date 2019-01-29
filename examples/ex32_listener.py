import time
from roslibpy import Topic
from compas_fab.backends import RosClient

client = RosClient()
client.run()

topic = Topic(client, '/messages', 'std_msgs/String')
topic.subscribe(print)

while True:
    time.sleep(1)

client.terminate()
