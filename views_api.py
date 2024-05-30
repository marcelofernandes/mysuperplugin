from http import HTTPStatus

import httpx
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.decorators import WalletTypeInfo, get_key_type
# from lnbits.core.services import pay_invoice
import paho.mqtt.client as mqtt # type: ignore
import time

from .models import Example

# views_api.py is for you API endpoints that could be hit by another service

mysuperplugin_ext_api = APIRouter(
    prefix="/api/v1",
    tags=["mysuperplugin"],
)


@mysuperplugin_ext_api.get("/test/{mysuperplugin_data}", description="Example API endpoint")
async def api_mysuperplugin(mysuperplugin_data: str) -> Example:
    # Do some python things and return the data
    return Example(id="1", wallet=mysuperplugin_data)


@mysuperplugin_ext_api.get("/vetted", description="Get the vetted extension readme")
async def api_get_vetted(wallet: WalletTypeInfo = Depends(get_key_type)):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://raw.githubusercontent.com/marcelofernandes/lnbits-extensions/main/README.md"
            )
            return resp.text
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e

@mysuperplugin_ext_api.get("/health-check", description="Health check")
async def api_get_health_check():
    print("Ok")
    return "Ok"

@mysuperplugin_ext_api.get("/payment", description="Makes a payment")
async def api_get_payment():
    try:
        async with httpx.AsyncClient() as client:
            scan = await client.get(
                "https://4e16-177-84-220-121.ngrok-free.app/api/v1/lnurlscan/marcelo@4e16-177-84-220-121.ngrok-free.app",
                headers= {
                    "accept": "application/json, text/plain, */*", "x-api-key": "8662f429b2cd4ca3a01ea2b6ed001979"
                }
            )
            scanJson = scan.json()
            pay = await client.post(
                "https://4e16-177-84-220-121.ngrok-free.app/api/v1/payments/lnurl",
                headers = {
                    "accept": "application/json, text/plain, */*", "x-api-key": "8662f429b2cd4ca3a01ea2b6ed001979"
                },
                json = {
                    "amount": scanJson['minSendable'],
                    "callback": scanJson['callback'],
                    "comment": "",
                    "description": scanJson['description'],
                    "description_hash": scanJson['description_hash'],
                    "unit": 'sat'
                }
            )
            return pay.json()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
    
@mysuperplugin_ext_api.get("/mqtt", description="Makes a mqtt connect")
async def api_get_mqtt():
    print("get mqtt")
    try:
        # Callback para quando o cliente receber uma resposta CONNACK do servidor.
        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")
            # Subscribir ao tópico "test/topic"
            client.subscribe("test/topic")

        # Callback para quando uma mensagem é recebida do servidor.
        def on_message(client, userdata, msg):
            print(f"{msg.topic} {msg.payload.decode()}")

        def on_fail(client, userdata, flags, rc):
            print(f"Not Connected with result code {rc}")

        # Criar uma instância do cliente MQTT
        client = mqtt.Client()

        # Atribuir callbacks
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_connect_fail = on_fail

        # Conectar ao broker
        client.connect("172.21.240.91", 1883, 600)

        # Iniciar o loop para processar callbacks e manter a conexão aberta
        client.loop_start()
        return "MQTT Ok"
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e