import asyncio
from asyncio_mqtt import Client, MqttError # type: ignore

broker_address = '172.21.240.91'
port = 1883
topic = 'lnbits/example'

async def connect_and_subscribe():
    async with Client(broker_address, port) as client:
        await client.subscribe(topic)
        print(f'Subscrito no tópico {topic}')
        
        async with client.filtered_messages(topic) as messages:
            async for message in messages:
                print(f'Mensagem recebida: {message.payload.decode()}')

