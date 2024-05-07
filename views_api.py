from http import HTTPStatus

import httpx
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.decorators import WalletTypeInfo, get_key_type
from lnbits.core.services import pay_invoice

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

@mysuperplugin_ext_api.get("/payment", description="Makes a payment")
async def api_get_payment():
    try:
        async with httpx.AsyncClient() as client:
            scan = await client.get(
                "https://5949-177-84-220-121.ngrok-free.app/api/v1/lnurlscan/marcelo@5949-177-84-220-121.ngrok-free.app",
                headers= {
                    "accept": "application/json, text/plain, */*", "x-api-key": "90a427aa761447a5b322cd99727a4db6"
                }
            )
            scanJson = scan.json()
            pay = await client.post(
                "https://5949-177-84-220-121.ngrok-free.app/api/v1/payments/lnurl",
                headers = {
                    "accept": "application/json, text/plain, */*", "x-api-key": "90a427aa761447a5b322cd99727a4db6"
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
    