import asyncio

from fastapi import APIRouter # type: ignore
from lnbits.db import Database # type: ignore
from lnbits.tasks import create_permanent_unique_task # type: ignore
from loguru import logger # type: ignore

from .tasks import wait_for_paid_invoices
from .views import mysuperplugin_ext_generic
from .views_api import mysuperplugin_ext_api

import paho.mqtt.client as mqtt # type: ignore

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

# Callback para quando o cliente receber uma resposta CONNACK do servidor.
#def on_connect(client, userdata, flags, rc):
    #print(f"Connected with result code {rc}")
    # Subscribir ao tópico "test/topic"
    #client.subscribe("test/topic")

# Callback para quando uma mensagem é recebida do servidor.
#def on_message(client, userdata, msg):
    #print(f"{msg.topic} {msg.payload.decode()}")

# Criar uma instância do cliente MQTT
client = mqtt.Client()

# Atribuir callbacks
# client.on_connect = on_connect
#client.on_message = on_message

# Conectar ao broker
print(client)
# try:
#     client.connect("172.21.240.91", 1883, 600)
# except Exception as ex:
#     print(ex)


# Iniciar o loop para processar callbacks e manter a conexão aberta
#client.loop_forever()