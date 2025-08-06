from fastapi import HTTPException, Header

from app.core.config import settings

API_KEY_NAME = "X-API-KEY"
API_KEY_VALUE = settings.API_KEY


async def verify_api_key(x_api_key: str = Header(..., alias=API_KEY_NAME)):
    if x_api_key != API_KEY_VALUE:
        raise HTTPException(status_code=401, detail="Unauthorized")

