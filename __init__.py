import asyncio

from fastapi import APIRouter # type: ignore
from lnbits.db import Database # type: ignore
from lnbits.tasks import create_permanent_unique_task # type: ignore
from loguru import logger # type: ignore

from .tasks import wait_for_paid_invoices, example_task
from .views import mysuperplugin_ext_generic
from .views_api import mysuperplugin_ext_api
import paho.mqtt.client as mqtt # type: ignore
from typing import Callable
from lnbits.tasks import create_permanent_task # type: ignore
from lnbits.tasks import catch_everything_and_restart # type: ignore

broker = "172.21.240.91"
port = 1883
topic = "test/topic"

# async def print_message():
#     while True:
#         print("Mensagem impressa a cada 3 segundos")
#         await asyncio.sleep(3)

# # Função principal para inicializar a tarefa de impressão
# async def main():
#     # Criar um novo loop de eventos asyncio
#     loop = asyncio.new_event_loop()

#     # Definir o loop de eventos asyncio como o loop atual
#     asyncio.set_event_loop(loop)

#     # Iniciar a tarefa de impressão no loop de eventos asyncio
#     asyncio.create_task(print_message())

#     # Executar o loop de eventos asyncio indefinidamente
#     loop.run_forever()

# # Executar a função principal
# main()

# def initialize_server_websocket_logger() -> Callable:
#     async def update_websocket_serverlog():
#         while True:
#             print("Running")
#             await asyncio.sleep(2)

#     return update_websocket_serverlog

# server_log_task = initialize_server_websocket_logger()
# create_permanent_task(server_log_task)
# print("Permanent Task created")

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

# async def startup_event():
#     print("test")

# task2 = create_permanent_unique_task("ext_mqtt2", startup_event)  # type: ignore
# scheduled_tasks.append(task2)

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
    loop = asyncio.get_event_loop()
    loop.create_task(catch_everything_and_restart(example_task))
    # task3 = create_permanent_unique_task("ext_mytask3", example_task)
    # scheduled_tasks.append(task3)

# # Configuração do Cliente MQTT
# def on_connect(client, userdata, flags, rc):
#     print("Conectado com código de resultado: " + str(rc))
#     client.subscribe(topic)

# def on_message(client, userdata, msg):
#     mensagem = msg.payload.decode()
#     print(f"Mensagem recebida: {mensagem} no tópico {msg.topic}")
#     # Colocar a mensagem na fila
#     asyncio.run_coroutine_threadsafe(userdata.put(mensagem), userdata._loop)

# def on_log(client, userdata, level, buf):
#     print(f"Log: {buf}")

# # Coroutine para processar a mensagem
# async def process_message(queue):
#     while True:
#         mensagem = await queue.get()
#         if mensagem is None:
#             break
#         # Exemplo de integração com os serviços do LNbits
#         await asyncio.sleep(3)

# # Função para rodar o loop do MQTT em uma thread separada
# def mqtt_thread(loop, queue):
#     asyncio.set_event_loop(loop)
#     loop.create_task(mqtt_loop(queue))
#     loop.run_forever()

# # Função para rodar o loop do MQTT
# async def mqtt_loop(queue):
#     client = mqtt.Client(userdata=queue)
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.on_log = on_log  # Associa o callback de log

#     client.connect(broker, 1883, 60)
#     client.loop_start()

#     while True:
#         await asyncio.sleep(1)  # Manter o loop rodando

# # Função principal para inicializar as tarefas
# async def main():
#     queue = asyncio.Queue()
#     loop = asyncio.new_event_loop()

#     # Iniciar uma nova thread com um novo loop de eventos
#     threading.Thread(target=mqtt_thread, args=(loop, queue), daemon=True).start()

#     await process_message(queue)

# # Criar a tarefa principal
# create_permanent_task(main)
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