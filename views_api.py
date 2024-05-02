from http import HTTPStatus

import httpx
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.decorators import WalletTypeInfo, get_key_type
from lnbits import Wallet

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
    server_url = "http://localhost:5000"
    api_key = "120c458e98fa436da99a182fb4adf10a"
    wallet = Wallet(server_url, api_key)

    # ID do invoice que você deseja pagar
    invoice_id = "lnbcrt1u1pnr8e38pp55239fcmpfz4njxt740xjf7sp8neavnlmkzsyfrzanjme377776psdqqcqzzsxqyz5vqsp552j8kuqz60v5g0mlg0r9c74xmvhc4cxryplrja9qr8lpzgdgpevq9qyyssqak4exelqw3tcwcq7elfkuf3tw58hlfaxxfpr2g3wgllu5rxuqgqq8zm5rgucasyamrdgsm3sfcuf6ftpukv9y0qwgy86jwg95xkd96cqhu5kps"

    # Valor do pagamento em satoshis
    valor_pagamento = 100  # Por exemplo, 10.000 satoshis

    # Enviar o pagamento do invoice
    resposta_pagamento = await wallet.pay_invoice(invoice_id, valor_pagamento)

    # Verificar se o pagamento foi bem-sucedido
    if resposta_pagamento.get("payment_error"):
        return resposta_pagamento
    else:
        return "Pagamento enviado com sucesso!"