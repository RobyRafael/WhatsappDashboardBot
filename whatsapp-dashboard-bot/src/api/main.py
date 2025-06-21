from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import os
import aiofiles
from datetime import datetime
import logging
from ..bot.whatsapp_bot import WhatsAppBot
from ..bot.config import API_CONFIG
from .models.schemas import MessageRequest, MessageResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsApp Dashboard Bot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# WhatsApp Bot instance
bot = None

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_CONFIG["api_key"]:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.on_event("startup")
async def startup_event():
    global bot
    try:
        # Use unique user data directory for API instance
        bot = WhatsAppBot(user_data_suffix="api")
        logger.info("WhatsApp Bot initialized for API")
    except Exception as e:
        logger.error(f"Failed to initialize WhatsApp Bot: {e}")
        bot = None

@app.on_event("shutdown")
async def shutdown_event():
    global bot
    if bot:
        bot.close()
    logger.info("WhatsApp Bot closed")

@app.post("/api/messages", response_model=MessageResponse)
async def send_message(request: MessageRequest, api_key: str = Depends(get_api_key)):
    """Send WhatsApp message"""
    try:
        if not bot:
            raise HTTPException(status_code=503, detail="WhatsApp Bot not available")
            
        result = bot.send_message(request.phone_number, request.message)
        return MessageResponse(**result, timestamp=datetime.now())
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/media")
async def upload_media(
    file: UploadFile = File(...),
    phone_number: str = Form(None),
    caption: str = Form(""),
    api_key: str = Depends(get_api_key)
):
    """Upload and send media file"""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = "./media/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save uploaded file
        file_path = os.path.join(upload_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Send media if phone number provided
        if phone_number and bot:
            result = bot.send_media(phone_number, file_path, caption)
            return {
                "file_path": file_path,
                "send_result": result,
                "timestamp": datetime.now()
            }
        
        return {
            "file_path": file_path,
            "message": "File uploaded successfully",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error uploading media: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now(),
        "bot_status": "available" if bot else "unavailable"
    }

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "WhatsApp Dashboard Bot API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "messages": "/api/messages",
            "media": "/api/media",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_CONFIG["host"], port=API_CONFIG["port"])