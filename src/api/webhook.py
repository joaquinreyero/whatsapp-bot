import json

from fastapi import Request, HTTPException, Depends, APIRouter, Query

from src.schema.webhook import WebhookPayload
from src.decorator.security import signature_required
from src.utils.whatsapp import process_whatsapp_message, is_valid_whatsapp_message
from src.config import Settings

router = APIRouter(
    prefix="/api/v1/webhook",
    tags=['Webhooks']
)


@router.post("/", dependencies=[Depends(signature_required)])
async def handle_message(request: Request, payload: WebhookPayload):
    body = payload.dict()
    if body.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("statuses"):
        return {"status": "ok"}
    try:
        if is_valid_whatsapp_message(body):
            process_whatsapp_message(body)
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=404, detail="Not a WhatsApp API event")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON provided")


@router.get("/")
async def verify_webhook(hub_mode: str = Query(...), hub_verify_token: str = Query(...), hub_challenge: str = Query(...)):
    if hub_mode == "subscribe" and hub_verify_token == Settings().VERIFY_TOKEN:
        return hub_challenge
    else:
        raise HTTPException(status_code=400, detail="Invalid token or mode")
