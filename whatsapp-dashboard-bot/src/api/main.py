from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import logging
import shutil
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bot.whatsapp_bot import WhatsAppBot
from bot.config import API_CONFIG

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

# Pydantic models
class MessageRequest(BaseModel):
    phone_number: str
    message: str

class MessageResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime = datetime.now()

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_CONFIG["api_key"]:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.on_event("startup")
async def startup_event():
    global bot
    try:
        # Gunakan instance WhatsAppBot TANPA suffix untuk menggunakan session yang sama
        # dengan testing.py dan login_whatsapp.py (folder chrome_user_data yang sama)
        logger.info("🚀 Inisialisasi WhatsApp Bot untuk API...")
        bot = WhatsAppBot()  # Tidak ada user_data_suffix, gunakan chrome_user_data default
        
        # Menggunakan metode login dari testing.py
        if bot.driver:
            logger.info("Memulai proses login WhatsApp Web...")
            print("🚀 Memulai proses login WhatsApp Web...")
            
            # Cek environment headless
            headless = os.getenv("HEADLESS", "false").lower() == "true"
            if headless:
                logger.info("💡 Running in headless mode - session harus sudah ada dari login manual")
                print("💡 Running in headless mode - session harus sudah ada dari login manual")
            
            if bot.login():
                logger.info("✅ WhatsApp Bot berhasil login untuk API")
                print("✅ WhatsApp Bot berhasil login untuk API")
            else:
                if headless:
                    logger.warning("⚠️ WhatsApp Bot gagal login - perlu login manual menggunakan script login_whatsapp.py")
                    print("⚠️ WhatsApp Bot gagal login - perlu login manual menggunakan script login_whatsapp.py")
                else:
                    logger.warning("⚠️ WhatsApp Bot gagal login otomatis - perlu login manual")
                    print("⚠️ WhatsApp Bot gagal login otomatis - perlu login manual")
        else:
            logger.error("❌ Failed to initialize Chrome driver")
            print("❌ Failed to initialize Chrome driver")
            
    except Exception as e:
        logger.error(f"Failed to initialize WhatsApp Bot: {e}")
        print(f"❌ Failed to initialize WhatsApp Bot: {e}")
        bot = None

@app.on_event("shutdown")
async def shutdown_event():
    global bot
    if bot:
        bot.close()
    logger.info("WhatsApp Bot closed")

@app.post("/api/messages", response_model=MessageResponse)
async def send_message(request: MessageRequest, api_key: str = Depends(get_api_key)):
    """Send WhatsApp message dengan detailed logging"""
    if not bot:
        raise HTTPException(status_code=503, detail="WhatsApp Bot not available")
    
    logger.info(f"🔍 API Request - Phone: {request.phone_number}, Message: '{request.message}'")
    print(f"🔍 API Request - Phone: {request.phone_number}, Message: '{request.message}'")
    
    try:
        result = bot.send_message(request.phone_number, request.message)
        
        logger.info(f"🔍 Bot Response: {result}")
        print(f"🔍 Bot Response: {result}")
        
        if result['status'] == 'success':
            logger.info(f"✅ API Success: {result['message']}")
            print(f"✅ API Success: {result['message']}")
            return MessageResponse(status="success", message=result['message'])
        else:
            logger.error(f"❌ API Error: {result['message']}")
            print(f"❌ API Error: {result['message']}")
            raise HTTPException(status_code=400, detail=result['message'])
            
    except Exception as e:
        logger.error(f"❌ API Exception: {str(e)}")
        print(f"❌ API Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/api/media")
async def upload_media(
    file: UploadFile = File(...),
    phone_number: str = Form(None),
    caption: str = Form(""),
    api_key: str = Depends(get_api_key)
):
    """Upload and send media file"""
    if not bot:
        raise HTTPException(status_code=503, detail="WhatsApp Bot not available")
    
    if not phone_number:
        raise HTTPException(status_code=400, detail="Phone number is required")
    
    try:
        # Create upload directory if it doesn't exist
        upload_dir = "media/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save uploaded file
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Send media using bot
        result = bot.send_media(phone_number, file_path, caption)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        if result['status'] == 'success':
            return {"status": "success", "message": result['message']}
        else:
            raise HTTPException(status_code=400, detail=result['message'])
            
    except Exception as e:
        logger.error(f"Error uploading media: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint dengan status login"""
    bot_status = "unavailable"
    login_status = "unknown"
    
    if bot and bot.driver:
        bot_status = "available"
        # Cek login status menggunakan metode testing.py
        try:
            if bot.check_login_status():
                login_status = "logged_in"
            else:
                login_status = "not_logged_in"
        except:
            login_status = "check_failed"
    
    return {
        "status": "healthy", 
        "timestamp": datetime.now(),
        "bot_status": bot_status,
        "login_status": login_status,
        "session_info": {
            "user_data_dir": "chrome_user_data",
            "profile": "WhatsApp",
            "headless": os.getenv("HEADLESS", "false").lower() == "true"
        }
    }

@app.get("/api/login-status")
async def check_login_status_endpoint(api_key: str = Depends(get_api_key)):
    """Endpoint khusus untuk cek status login"""
    if not bot:
        raise HTTPException(status_code=503, detail="WhatsApp Bot not available")
    
    try:
        is_logged_in = bot.check_login_status()
        qr_status = bot.get_qr_code_status()
        
        return {
            "logged_in": is_logged_in,
            "qr_status": qr_status,
            "timestamp": datetime.now(),
            "session_info": {
                "user_data_dir": "chrome_user_data",
                "profile": "WhatsApp",
                "headless": os.getenv("HEADLESS", "false").lower() == "true"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/debug")
async def debug_whatsapp(api_key: str = Depends(get_api_key)):
    """Debug endpoint untuk melihat status WhatsApp Web"""
    if not bot:
        raise HTTPException(status_code=503, detail="WhatsApp Bot not available")
    
    try:
        # Force debug
        bot.debug_page_elements()
        
        current_url = bot.driver.current_url if bot.driver else "No driver"
        page_title = bot.driver.title if bot.driver else "No title"
        
        return {
            "current_url": current_url,
            "page_title": page_title,
            "login_status": bot.check_login_status(),
            "qr_status": bot.get_qr_code_status(),
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "WhatsApp Dashboard Bot API",
        "version": "1.0.0",
        "session_shared": True,
        "user_data_dir": "chrome_user_data",
        "endpoints": {
            "health": "/api/health",
            "send_message": "/api/messages",
            "send_media": "/api/media",
            "login_status": "/api/login-status",
            "debug": "/api/debug",
            "docs": "/docs"
        },
        "instructions": {
            "login": "Use login_whatsapp.py script to login first, then API will use the same session",
            "session": "All scripts (testing.py, login_whatsapp.py, API) share the same Chrome session in chrome_user_data folder"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_CONFIG["host"], port=API_CONFIG["port"])