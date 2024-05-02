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
    pr = "lnbcrt1u1pnr8u9zpp5v2zexmglqay2cez780akc235wd8m4y9kc3azpnxvwn56x9wl625sdqqcqzzsxqyz5vqsp5dp4lz86ajvk5tgx4qktda2cqavur4nhjxm0l3nnj5mjmda0dwe5q9qyyssqc5fuvuwcsjsmr3nstvuh6ja7lfmgahpcgly350k90kthlntjlnl37ljpp4mwcnuz8el98le5y2pzcxuhrzadq2zs8ufyv2pty23z2mgpcy22fa"
    resposta_pagamento = await pay_invoice(
            wallet_id=wallet_id,
            payment_request=pr,
        )
    return resposta_pagamento