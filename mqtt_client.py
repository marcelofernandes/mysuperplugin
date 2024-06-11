import paho.mqtt.client as mqtt
from loguru import logger
from threading import Thread
from .crud import (create, update, get_device, delete_device)
import asyncio

class MQTTClient:
    def __init__(self):
        self.broker = "172.21.240.91"
        self.port = 1883
        self.topic_payment = "topic/payment"
        self.topic_device = "topic/device"
        self.client = None
        # try:
        #     loop = asyncio.get_running_loop()
        # except RuntimeError:
        #     loop = None
        # if loop and loop.is_running():
        #     asyncio.run_coroutine_threadsafe(create("payment_01"), loop)
        # else:
        #     loop = asyncio.new_event_loop()
        #     asyncio.run_coroutine_threadsafe(create("payment_01"), loop)

    def _ws_handlers(self):
            def on_connect(client, userdata, flags, rc):
                logger.info("Conectado com código de resultado: " + str(rc))
                client.subscribe(self.topic_payment)

            async def test(msg, loop):
                await asyncio.run_coroutine_threadsafe(handle_message(msg), loop)

            async def handle_message(msg):
                msg_decoded = msg.payload.decode() 
                await create(msg_decoded)
                self.client.publish(self.topic_device, f"Device {msg_decoded} liberado")

            def on_message(client, userdata, msg):
                message = f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}"
                asyncio.run(handle_message(msg))
                logger.info(message)

            return on_connect, on_message

    def connect_to_mqtt_broker(self):
        logger.debug(f"Connecting to MQTT broker")
        on_connect, on_message = self._ws_handlers()
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(self.broker, self.port, 60)
    
    def start_mqtt_client(self):
        wst = Thread(target=self.client.loop_start)
        wst.daemon = True
        wst.start()

    def disconnect_to_mqtt_broker(self):
        self.client.loop_stop()
        self.client.disconnect()
