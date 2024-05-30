# mysuperplugin/mqtt_client.py

import paho.mqtt.client as mqtt # type: ignore
import asyncio

class MQTTClient:
    def __init__(self, broker_url, broker_port):
        self.client = mqtt.Client()
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            # Inscrever-se em um tópico após a conexão com o broker
            client.subscribe("test/topic")
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"Subscribed: {mid} QoS: {granted_qos}")

    async def connect(self):
        self.client.connect(self.broker_url, self.broker_port, 60)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.client.loop_forever)

# Configurar o cliente MQTT
mqtt_client = MQTTClient(broker_url="172.21.240.91", broker_port=1883)
asyncio.run(mqtt_client.connect())
