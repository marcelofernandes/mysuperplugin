# tasks.py is for asynchronous when invoices get paid

# add your dependencies here

import asyncio

from lnbits.core.models import Payment
from lnbits.tasks import register_invoice_listener
from loguru import logger

from .mqtt_client import mqtt_client

async def wait_for_paid_invoices():
    invoice_queue = asyncio.Queue()
    register_invoice_listener(invoice_queue, "mysuperplugin")

    while True:
        payment = await invoice_queue.get()
        await on_invoice_paid(payment)

async def wait_for_mqtt():
    invoice_queue = asyncio.Queue()
    register_invoice_listener(invoice_queue, "mysuperplugin2")
    asyncio.create_task(mqtt_client.connect())

async def on_invoice_paid(payment: Payment) -> None:
    if (
        payment.extra.get("tag") == "mysuperplugin"
    ):  # Will grab any payment with the tag "mysuperplugin"
        logger.debug(payment)
