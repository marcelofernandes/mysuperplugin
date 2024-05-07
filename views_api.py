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
    wallet_id = "1155c6eb19a04a74a61a4c42e1d8323c"
    pr = "lnbcrt1u1pnr8uwxpp55ayhd6e8m7t5xmmk6z6v5qglx7pcjgzy20v5u9xz6rugpue80gdsdqqcqzzsxqyz5vqsp5m6p6mvmqwgsjn86c62tsucjz595vxvgzdeu6vnqpswlvsz7ggxjs9qyyssqe04rg7xewfxxkq64karujsmyp5ghq5yfm8mtze5e0ylc3dnhm67shkf3l9au9jhtuerv3e6m0pnl56wjkmk6v854d9h7k8axefksycqp88ywgr"
    resposta_pagamento = await pay_invoice(
            wallet_id=wallet_id,
            payment_request=pr,
        )
    return resposta_pagamento

# @mysuperplugin_ext_api.get("/payment2", description="Makes a payment")
# async def api_get_payment2():
#     try:
#         async with httpx.AsyncClient() as client:
#             resp = await client.get(
#                 "https://5949-177-84-220-121.ngrok-free.app/api/v1/lnurlscan/marcelo@5949-177-84-220-121.ngrok-free.app",
#                 headers: {
#                     "accept": "application/json, text/plain, */*", "x-api-key": "90a427aa761447a5b322cd99727a4db6"
#                 }
#             )
#             return resp
#     except Exception as e:
#         raise HTTPException(
#             status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
#         ) from e
    