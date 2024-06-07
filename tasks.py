# tasks.py is for asynchronous when invoices get paid

# add your dependencies here

import asyncio
import time
from lnbits.core.models import Payment
from lnbits.tasks import register_invoice_listener
from loguru import logger
import paho.mqtt.client as mqtt # type: ignore
from .mqtt_client import test_client
from concurrent.futures import ThreadPoolExecutor

async def wait_for_paid_invoices():
    invoice_queue = asyncio.Queue()
    register_invoice_listener(invoice_queue, "mysuperplugin")

    while True:
        payment = await invoice_queue.get()
        await on_invoice_paid(payment)


async def on_invoice_paid(payment: Payment) -> None:
    if (
        payment.extra.get("tag") == "mysuperplugin"
    ):  # Will grab any payment with the tag "mysuperplugin"
        logger.debug(payment)

broker = "172.21.240.91"
port = 1883
topic = "test/topic"

def on_connect(client, userdata, flags, rc):
    logger.info("Conectado com código de resultado: " + str(rc))
    client.subscribe(topic)

# async def print_message(message, loop):
#     async def pmessage(messag):
#         print("Print new 8: " + messag)
#     task = loop.create_task(pmessage(message))
#     await task

# def on_message(client, userdata, msg):
#     message = f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}"
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = None
#     if loop and loop.is_running():
#         loop.run_until_complete(print_message(message))
#     else:
#         loop = asyncio.new_event_loop()
#         loop.run_until_complete(print_message(message))
#         logger.info("Run coroutine threadsafe")

# def on_message(client, userdata, msg):
#     message = f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}"
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = None
#     if loop and loop.is_running():
#         loop.run_until_complete(print_message(message, loop))
#         # print_message(message, loop)
#     else:
#         logger.info("Run coroutine threadsafe")
#         loop = asyncio.new_event_loop()
#         loop.run_until_complete(print_message(message, loop))

async def print_message(message):
    asyncio.sleep(1)
    print("Print new 8: " + message)

def on_message(client, userdata, msg):
    message = f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}"
    async def pmessage(messa):
        asyncio.sleep(1)
        logger.info(messa)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        logger.info("if statement")
        asyncio.run(pmessage(message))
    else:
        logger.info("else statement")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run(pmessage(message))

async def example_task():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_start()