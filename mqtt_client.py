import paho.mqtt.client as mqtt
import asyncio

class MQTTClient:
    def __init__(self, broker_url, broker_port):
        self.client = mqtt.Client()
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("test/topic")

    def on_message(self, client, userdata, msg):
        print(f"{msg.topic} {msg.payload.decode()}")

    async def connect(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.client.connect, self.broker_url, self.broker_port, 60)
        await loop.run_in_executor(None, self.client.loop_forever)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

# Configuração do cliente MQTT
broker_address = "172.21.240.91"  # Substitua pelo endereço do seu broker
port = 1883                   # Substitua pela porta usada pelo seu broker

mqtt_client = MQTTClient(broker_address, port)
