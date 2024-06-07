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
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        coro = asyncio.sleep(1, result=3)

        # Submit the coroutine to a given loop
        future = asyncio.run_coroutine_threadsafe(coro, loop)

        # Wait for the result with an optional timeout argument
        assert future.result() == 3
        logger.info("Assert true and loop running")
    else:
        loop = asyncio.new_event_loop()
        coro = asyncio.sleep(1, result=3)

        # Submit the coroutine to a given loop
        future = asyncio.run_coroutine_threadsafe(coro, loop)

        # Wait for the result with an optional timeout argument
        assert future.result() == 3
        logger.info("Assert true")
    
    # with ThreadPoolExecutor() as pool:
    #     await loop.run_in_executor(pool, print_message(message))
    #     print("Terminated")

async def example_task():
    print(asyncio.get_event_loop())
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_start()