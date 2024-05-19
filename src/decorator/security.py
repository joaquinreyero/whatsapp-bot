from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer
import hashlib
import hmac
import os


class SignatureHeader(HTTPBearer):
    async def __call__(self, request: Request):
        authorization: str = await super().__call__(request)
        return authorization.credentials[7:]  # Removing 'sha256='


def validate_signature(payload, signature):
    expected_signature = hmac.new(
        bytes(os.getenv("APP_SECRET"), "latin-1"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)


async def signature_required(request: Request, signature: str = Depends(SignatureHeader())):
    payload = await request.body()
    if not validate_signature(payload.decode("utf-8"), signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
