import asyncio

from fastapi import APIRouter # type: ignore
from lnbits.db import Database # type: ignore
from lnbits.tasks import create_permanent_unique_task # type: ignore
from loguru import logger # type: ignore

from .tasks import wait_for_paid_invoices
from .views import mysuperplugin_ext_generic
from .views_api import mysuperplugin_ext_api
import paho.mqtt.client as mqtt # type: ignore
import asyncio
import time

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

async def tarefa_background():
    def on_subscribe(client, userdata, flags, rc):
        print(f"Subscribed with result code {rc}")

    def on_unsubscribe(client, userdata, mid):
        print(f"Inscrição cancelada no tópico")

    def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        if rc == 0:
            print("Successfully connected to broker")
        else:
            print(f"Failed to connect, return code {rc}")
        client.on_subscribe = on_subscribe
        client.on_unsubscribe = on_unsubscribe
        client.subscribe("test/topic")

    def on_message(client, userdata, msg):
        print(f"{msg.topic} {msg.payload.decode()}")

    def on_fail(client, userdata, flags, rc):
        print(f"Not Connected with result code {rc}")

    def on_log(client, userdata, flags, rc):
        print(f"Log: {rc}")

    client = mqtt.Client()

    # Atribuir callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_connect_fail = on_fail
    client.on_log = on_log

    # Conectar ao broker
    client.connect("172.21.240.91", 1883, 600)

    print("Loop start")
    # Iniciar o loop para processar callbacks e manter a conexão aberta
    client.loop_start()
    while True:
        await asyncio.sleep(5)

async def main():
    # Inicia a tarefa em background
    asyncio.create_task(tarefa_background())
    
    # Código principal continua rodando
    print("Código principal está rodando")
    await asyncio.sleep(20)
    print("Código principal terminou")

# Executa o loop de eventos
asyncio.run(main())

# def on_subscribe(client, userdata, flags, rc):
#     print(f"Subscribed with result code {rc}")

# def on_connect(client, userdata, flags, rc):
#     print(f"Connected with result code {rc}")
#     if rc == 0:
#         print("Successfully connected to broker")
#     else:
#         print(f"Failed to connect, return code {rc}")
#     client.on_subscribe = on_subscribe
#     client.subscribe("test/topic")

# def on_message(client, userdata, msg):
#     print(f"{msg.topic} {msg.payload.decode()}")

# def on_fail(client, userdata, flags, rc):
#     print(f"Not Connected with result code {rc}")

# def on_disconnect(client, userdata, flags, rc):
#     print(f"Disconected with result code {rc}")

# def mqtt_client_thread():
#     client = mqtt.Client()
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.on_fail = on_fail
#     client.on_disconnect = on_disconnect
    
#     try:
#         client.connect("172.21.240.91", 1883, 60)
#         client.loop_forever()
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#     client.connect("172.21.240.91", 1883, 600)
#     client.loop_forever()

# client = mqtt.Client()

# client.on_connect = on_connect
# client.on_message = on_message
# client.on_connect_fail = on_fail

# client.connect("172.21.240.91", 1883, 600)

# client.loop_start()
# time.sleep(20)

# mqtt_thread = threading.Thread(target=mqtt_client_thread)
# mqtt_thread.start()

