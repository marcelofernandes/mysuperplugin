# tasks.py is for asynchronous when invoices get paid

# add your dependencies here

import asyncio

from lnbits.core.models import Payment
from lnbits.tasks import register_invoice_listener
from loguru import logger
import paho.mqtt.client as mqtt # type: ignore


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

async def on_connect(client, userdata, flags, rc):
    await asyncio.sleep(0.5)
    print("Connected")
    # logger.info("Conectado com código de resultado: " + str(rc))
    client.subscribe(topic)

async def on_message(client, userdata, msg):
    await asyncio.sleep(0.5)
    print("Message rec")
    # logger.info(f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}")

async def example_task():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_start()