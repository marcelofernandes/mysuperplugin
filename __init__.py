import asyncio

from fastapi import APIRouter # type: ignore
from lnbits.db import Database # type: ignore
from lnbits.tasks import create_permanent_unique_task # type: ignore
from loguru import logger # type: ignore

from .tasks import wait_for_paid_invoices
from .views import mysuperplugin_ext_generic
from .views_api import mysuperplugin_ext_api
import paho.mqtt.client as mqtt # type: ignore
from lnbits.tasks import create_permanent_task # type: ignore
from typing import Callable

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

def on_subscribe(client, userdata, flags, rc):
    print("Subscribed!")

# Configuração do Cliente MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado com código de resultado: " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    print(f"Mensagem recebida: {mensagem} no tópico {msg.topic}")
    # Colocar a mensagem na fila
    userdata.put_nowait(mensagem)

# Coroutine para processar a mensagem
async def process_message(queue):
    while True:
        mensagem = await queue.get()
        if mensagem is None:
            break
        # Exemplo de integração com os serviços do LNbits
        await asyncio.sleep(10)

# Função para rodar o loop do MQTT
async def mqtt_loop(queue):
    client = mqtt.Client(client_id="123121213",userdata=queue)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    client.connect(broker, port, 60)
    client.loop_start()

    while True:
        await asyncio.sleep(1)  # Manter o loop rodando

# Função que retorna a coroutine mqtt_loop
def start_mqtt_loop(queue):
    return mqtt_loop(queue)

# Função principal para inicializar as tarefas
async def main():
    queue = asyncio.Queue()
    create_permanent_task(lambda: start_mqtt_loop(queue))
    await process_message(queue)

# Criar a tarefa principal
create_permanent_task(main)

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