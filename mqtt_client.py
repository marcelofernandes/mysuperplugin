import asyncio
import paho.mqtt.client as mqtt # type: ignore
from loguru import logger # type: ignore
from threading import Thread

broker_address = '172.21.240.91'
port = 1883
topic = 'test/topic'

def test_client():
    return "Ok"

class MQTTClient:
    def __init__(self):
        self.running = False
        self.broker = "172.21.240.91"
        self.port = 1883
        self.topic = "test/topic"

    def _ws_handlers(self):
            def on_connect(client, userdata, flags, rc):
                logger.info("Conectado com código de resultado: " + str(rc))
                client.subscribe(self.topic)

            def on_message(client, userdata, msg):
                message = f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}"
                logger.info(message)

            return on_connect, on_message

    async def connect_to_mqtt_broker(self):
        logger.debug(f"Connecting to the broker...")
        on_connect, on_message = self._ws_handlers()
        await asyncio.sleep(5)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(self.broker, self.port, 60)
        wst = Thread(target=client.loop_start)
        wst.daemon = True
        wst.start()


# async def connect_and_subscribe(client):
#     await client.subscribe(topic)
#     print(f'Subscrito no tópico {topic}')
        
#     async with client.filtered_messages(topic) as messages:
#         async for message in messages:
#             print(f'Mensagem recebida: {message.payload.decode()}')
        

