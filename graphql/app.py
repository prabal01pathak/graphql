import os

from fastapi import FastAPI, Request, BackgroundTasks
from sse_starlette import EventSourceResponse
import websockets
from dotenv import load_dotenv
from pydantic import BaseModel
from azure.messaging.webpubsubservice import WebPubSubServiceClient

load_dotenv()

app = FastAPI()
connection_string = os.getenv("connection_string")


class CustomSchema(BaseModel):
    """ base model"""


HUB = set()

async def message_generator(request, url: str, hub) -> str:
    async with websockets.connect(url) as ws:
        while True:
            if await request.is_disconnected():
                print("client disconnected!!!")
                break
            resp = await ws.recv()
            yield resp


@app.get("/sse")
async def sse_endpoint(request: Request, hub: str) -> str:
    HUB.add(hub)
    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub)
    token = service.get_client_access_token()
    event_generator = message_generator(request, token["url"], hub)
    return EventSourceResponse(event_generator)


@app.post("/publish")
async def publish_message(message: CustomSchema, request: Request, background_task: BackgroundTasks):
    message = await request.json() 
    print("hubs: ", HUB)
    background_task.add_task(send_message, message)
    return {"sent_to": list(HUB)}


async def send_message(message: dict) -> ...:
    res = {}
    for hub in HUB:
        service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub)
        res = service.send_to_all(message, content_type='application/json')
    return res