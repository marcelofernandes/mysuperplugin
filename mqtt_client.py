# mysuperplugin/mqtt_client.py

import paho.mqtt.client as mqtt # type: ignore

class MQTTClient:
    def __init__(self, broker_url, broker_port):
        self.client = mqtt.Client()
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe("test/topic")
        def on_subscribe(self, client, userdata, flags, rc):
            print(f"Subscribed to MQTT broker with result code {rc}")
        client.on_subscribe = on_subscribe

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

    def connect(self):
        self.client.connect(self.broker_url, self.broker_port, 60)
        self.client.loop_start()

