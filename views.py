from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer

mysuperplugin_ext_generic = APIRouter(tags=["mysuperplugin"])

import paho.mqtt.client as mqtt # type: ignore

# Função de callback quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.topic} {msg.payload.decode()}")

# Configura o cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

# Conecta ao broker MQTT
mqtt_client.connect("172.21.240.91", 1883, 60)
mqtt_client.loop_start()

# Subscreve em um tópico
mqtt_client.subscribe("test/topic")


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
