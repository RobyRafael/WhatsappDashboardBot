from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MediaUploadSchema(BaseModel):
    filename: str
    path: str
    timestamp: str
    recipient: str

class MessageSchema(BaseModel):
    text: str
    media: Optional[List[str]] = None
    recipient: str

class ResponseSchema(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class MessageRequest(BaseModel):
    phone_number: str
    message: str

class MessageResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime

class MediaUploadResponse(BaseModel):
    file_path: str
    message: str
    timestamp: datetime
    send_result: Optional[dict] = None