import asyncio

from fastapi import APIRouter # type: ignore
from lnbits.db import Database # type: ignore
from lnbits.tasks import create_permanent_unique_task # type: ignore
from loguru import logger # type: ignore

from .tasks import wait_for_paid_invoices
from .views import mysuperplugin_ext_generic
from .views_api import mysuperplugin_ext_api
import paho.mqtt.client as mqtt # type: ignore
import threading

db = Database("ext_mysuperplugin")

scheduled_tasks: list[asyncio.Task] = []

mysuperplugin_ext: APIRouter = APIRouter(prefix="/mysuperplugin", tags=["mysuperplugin"])
mysuperplugin_ext.include_router(mysuperplugin_ext_generic)
mysuperplugin_ext.include_router(mysuperplugin_ext_api)

mysuperplugin_static_files = [
    {
        "path": "/mysuperplugin/static",
        "name": "mysuperplugin_static",
    }
]

async def startup_event():
    print("test")

task2 = create_permanent_unique_task("ext_mqtt2", startup_event)  # type: ignore
scheduled_tasks.append(task2)

def mysuperplugin_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)

def mysuperplugin_start():
    # ignore will be removed in lnbits `0.12.6`
    # https://github.com/lnbits/lnbits/pull/2417
    task = create_permanent_unique_task("ext_testing", wait_for_paid_invoices)  # type: ignore
    scheduled_tasks.append(task)


broker = "172.21.240.91"
port = 1883
topic = "test/topic"

# Callback para quando o cliente se conecta ao broker
def on_connect(client, userdata, flags, rc):
    print("Conectado com código de retorno:", rc)
    client.subscribe("test/topic")

# Callback para quando uma mensagem é recebida do broker
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico:", msg.topic)
    print("Payload:", msg.payload.decode())

# Função para rodar o loop MQTT em um thread separado
def start_mqtt_loop(client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(mqtt_loop(client))
    loop.run_forever()

# Função assíncrona para conectar e iniciar o loop MQTT
async def mqtt_loop(client):
    client.connect(broker_address, port)
    client.loop_start()

# Configuração do broker MQTT
broker_address = "mqtt.eclipse.org"
port = 1883

# Criação de um cliente MQTT
client = mqtt.Client()

# Configuração dos callbacks
client.on_connect = on_connect
client.on_message = on_message

# Iniciar o loop MQTT em um thread separado
mqtt_thread = threading.Thread(target=start_mqtt_loop, args=(client,))
mqtt_thread.start()

# Execução do loop principal asyncio
# if __name__ == "__main__":
#     asyncio.run(main())
# print("The name:", __name__)
# asyncio.run(main())
# try:
#     loop = asyncio.get_event_loop()
#     loop.run_forever()
# except KeyboardInterrupt:
#     print("Encerrando...")
#     client.loop_stop()  # Para o loop de rede
#     client.disconnect()  # Desconecta do broker