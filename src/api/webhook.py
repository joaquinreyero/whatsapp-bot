import json

from fastapi import Request, HTTPException, Depends, APIRouter, Query

from src.schema.webhook import WebhookPayload
from src.decorator.security import signature_required
from src.utils.whatsapp import WhatsAppClient
from src.config import Settings

router = APIRouter(
    prefix="/api/v1/webhook",
    tags=['Webhooks']
)


@router.post("/")
async def handle_message(request: Request):
    print("callback is being called")
    wtsapp_client = WhatsAppClient()
    data = await request.json()
    print("We received " + str(data))
    response = wtsapp_client.process_notification(data)
    if response["statusCode"] == 200:
        if response["body"] and response["from_no"]:
            reply = response["body"]
            print("\nreply is:" + reply)
            wtsapp_client.send_text_message(message=reply, phone_number=response["from_no"], )
            print("\nreply is sent to whatsapp cloud:" + str(response))

    return {"status": "success"}, 200


@router.get("/")
async def verify_webhook(request: Request):
    query_params = request.query_params
    hub_mode = query_params.get('hub.mode')
    hub_challenge = query_params.get('hub.challenge')
    hub_verify_token = query_params.get('hub.verify_token')

    if hub_mode == "subscribe" and hub_verify_token == Settings().VERIFY_TOKEN:
        return int(hub_challenge)
    else:
        raise HTTPException(status_code=400, detail="Invalid token or mode")
