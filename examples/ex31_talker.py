import time
from roslibpy import Topic
from compas_fab.backends import RosClient

client = RosClient()
client.run()
    
topic = Topic(client, '/messages', 'std_msgs/String')
topic.advertise()

while True:
    topic.publish(dict(data='Hello world'))
    time.sleep(1)

client.terminate()
