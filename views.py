from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer
import asyncio
from asyncio_mqtt import Client # type: ignore
from .mqtt_client import connect_and_subscribe

mysuperplugin_ext_generic = APIRouter(tags=["mysuperplugin"])

broker_address = '172.21.240.91'
port = 1883

# Configuração do cliente MQTT
mqtt_client = Client(broker_address, port)
loop = asyncio.get_event_loop()
loop.create_task(connect_and_subscribe())

@mysuperplugin_ext_generic.get(
    "/", description="Example generic endpoint", response_class=HTMLResponse
)
async def index(
    request: Request,
    user: User = Depends(check_user_exists),
):
    return template_renderer(["mysuperplugin/templates"]).TemplateResponse(
        request, "mysuperplugin/index.html", {"user": user.dict()}
    )
