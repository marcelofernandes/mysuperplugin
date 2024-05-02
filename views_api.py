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
    pr = "lnbcrt1u1pnr8mflpp5xj937mpnlg5d5lsw9axnthng29mc7r0f06vgay4jkcmcy6snw2eqdqqcqzzsxqyz5vqsp5qtqxj2chnl3emyu0afa0h5r6n50ukyj8etx4jk3j3yd2ay6j390s9qyyssqgaaw30d5ngwhgsu6apyzu4ey82r7fzac4xwf6f4angx0ssf4hnzqz36kye6fc5cc2arwlu28lnwpz9y63zc3hu4z8lrhr7486sq6wsqqpzpr6g"
    resposta_pagamento = await pay_invoice(
            wallet_id=wallet_id,
            payment_request=pr,
        )
    return resposta_pagamento