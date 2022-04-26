from django.apps import AppConfig
import sys
import os

from Adafruit_IO import MQTTClient


adafruitData = {
    'emotionData': [],
    'waterData': [],
}
maxEmo = 100
maxWater = 4
speed = [0]
client = None

class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

    def ready(self):
        global client
        AIO_FEED_IDS = ['emotion', 'water']
        AIO_USERNAME = os.environ['AIO_USERNAME']
        AIO_KEY = os.environ['AIO_KEY']

        def connected(client):
            print("Connection established successfully.")
            for feed in AIO_FEED_IDS:
                client.subscribe(feed)

        def subscribe(client, userdata, mid, granted_qos):
            print("Subscribed.")

        def disconnected(client):
            print("Disconnected.")
            sys.exit(1)

        def message(client, feed_id, payload):
            global adafruitData
            if feed_id == 'emotion':
                adafruitData['emotionData'].append(float(payload))
            elif feed_id == 'water':
                adafruitData['waterData'].append(float(payload))

        client = [MQTTClient(AIO_USERNAME, AIO_KEY)]
        client[0].on_connect = connected
        client[0].on_disconnect = disconnected
        client[0].on_message = message
        client[0].on_subscribe = subscribe
        client[0].connect()
        client[0].loop_background()