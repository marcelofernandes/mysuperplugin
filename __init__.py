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

# Função de callback para quando a conexão for estabelecida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao Broker!")
        client.subscribe(topic)
    else:
        print(f"Falha na conexão, código de retorno: {rc}")

# Função de callback para quando uma mensagem for recebida
async def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    await asyncio.sleep(1)  # Simulando uma operação assíncrona

# Adaptador para chamar funções assíncronas a partir de callbacks síncronos
def on_message_sync(client, userdata, msg):
    # Aqui nós garantimos que estamos usando o loop de eventos principal
    loop = asyncio.get_running_loop()
    asyncio.run_coroutine_threadsafe(on_message(client, userdata, msg), loop)

# Função de callback para quando a inscrição for confirmada
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Inscrição confirmada no tópico {topic} com QoS {granted_qos}")

# Função de callback para quando a inscrição for cancelada
def on_unsubscribe(client, userdata, mid):
    print(f"Inscrição cancelada no tópico {topic}")

# Cria um cliente MQTT
client = mqtt.Client()

# Atribui as funções de callback
client.on_connect = on_connect
client.on_message = on_message_sync
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe

# Conecta ao Broker
client.connect(broker, port, 60)

# Inicia o loop de rede em background
client.loop_start()
try:
    loop = asyncio.get_event_loop()
    loop.run_forever()
except KeyboardInterrupt:
    print("Encerrando...")
    client.loop_stop()  # Para o loop de rede
    client.disconnect()  # Desconecta do broker