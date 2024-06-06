# tasks.py is for asynchronous when invoices get paid

# add your dependencies here

import asyncio

from lnbits.core.models import Payment
from lnbits.tasks import register_invoice_listener
from loguru import logger
import paho.mqtt.client as mqtt # type: ignore
from .mqtt_client import test_client


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
    print("Connected")
    client.subscribe(topic)

async def print_message(message):
    print(message)

def on_message(client, userdata, msg):

    # logger.info(f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}")
    # teste = test_client()
    message = f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}"
    # asyncio.create_task(print_message(message))
    try:
        loop = asyncio.get_running_loop()
        logger.info("Has loop")
    except RuntimeError:  # Nenhum loop em execução
        logger.info("Without loop")
        loop = None

    if loop and loop.is_running():
        loop.run_until_complete(print_message(message))
        logger.info("Task created")
    else:
        loop = asyncio.new_event_loop()
        # loop.run_until_complete(print_message(message))
        # asyncio.set_event_loop(loop)
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(print_message(message))
        # loop.create_task(print_message(message))
        loop.run_until_complete(print_message(message))
        logger.info("Run coroutine threadsafe")

    # asyncio.run_coroutine_threadsafe(print_message(message), loop)
    # logger.info(f"Teste message reveived: {teste}")

async def example_task():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_start()
    try:
        loop = asyncio.get_running_loop()
        logger.info("Has loop")
    except RuntimeError:  # Nenhum loop em execução
        logger.info("Without loop")
        loop = None

    if loop and loop.is_running():
        logger.info("Run forever 1")
    else:
        loop = asyncio.new_event_loop()
        logger.info("Run forever 2")