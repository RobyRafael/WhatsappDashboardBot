from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.bot.whatsapp_bot import send_message_with_media

router = APIRouter()

class MessageRequest(BaseModel):
    phone_number: str
    message: str
    media_url: str = None

@router.post("/send-message")
async def send_message(request: MessageRequest):
    try:
        result = await send_message_with_media(request.phone_number, request.message, request.media_url)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))