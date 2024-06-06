# tasks.py is for asynchronous when invoices get paid

# add your dependencies here

import asyncio

from lnbits.core.models import Payment
from lnbits.tasks import register_invoice_listener
from loguru import logger


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

async def example_task():
    while True:
        # Lógica da tarefa que deve ser executada continuamente
        # logger.info("Executando tarefa de exemplo...")
        print("Executando tarefa de exemplo...")
        await asyncio.sleep(5)