import paho.mqtt.client as mqtt
from loguru import logger
from threading import Thread

broker_address = '172.21.240.91'
port = 1883
topic = 'topic/payment'

def test_client():
    return "Ok"

class MQTTClient:
    def __init__(self):
        self.running = False
        self.broker = "172.21.240.91"
        self.port = 1883
        self.topic = "test/topic"
        self.client = None

    def _ws_handlers(self):
            def on_connect(client, userdata, flags, rc):
                logger.info("Conectado com código de resultado: " + str(rc))
                client.subscribe(self.topic)

            def on_message(client, userdata, msg):
                message = f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}"
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

    # def disconnect_to_mqtt_broker(self):
    #     logger.debug(f"Disconnecting to MQTT broker")
    #     self.client.loop_stop()
    #     self.client.disconnect()
    #     logger.debug(f"Disconnected to MQTT broker")
