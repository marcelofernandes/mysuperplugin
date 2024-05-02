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
    pr = "lnbcrt2u1pnr8m66pp560mldj2793rdcedzjvmkhh3pcw0zje9y8g5mm36hak4txx2mvhpsdqqcqzzsxqyz5vqsp5s5fvath98m8p4z0esveusgvjdrc7k38v55ef3thf66evcnk4q4as9qyyssqqysuu9mh3xajdj2eh2eyzk96s8zqtlugkqjmdk9p9f5nca9yxjzjwvv8x35jxj68etvpm2j2nkhfmjzs9vmgwmhptugc2czq8j4ncqgq4356qs"
    resposta_pagamento = await pay_invoice(
            wallet_id=wallet_id,
            payment_request=pr,
        )
    return resposta_pagamento