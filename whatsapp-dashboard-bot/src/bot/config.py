import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_CONFIG = {
    "headless": os.getenv("HEADLESS", "false").lower() == "true",
    "user_data_dir": os.getenv("USER_DATA_DIR", "./User_Data"),
    "timeout": int(os.getenv("TIMEOUT", "30"))
}

# API Configuration
API_CONFIG = {
    "host": os.getenv("API_HOST", "0.0.0.0"),
    "port": int(os.getenv("API_PORT", "8001")),
    "api_key": os.getenv("API_KEY", "your-secret-api-key")
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    "host": os.getenv("DASHBOARD_HOST", "0.0.0.0"),
    "port": int(os.getenv("DASHBOARD_PORT", "5000")),
    "upload_folder": os.getenv("UPLOAD_FOLDER", "./media/uploads"),
    "max_file_size": int(os.getenv("MAX_FILE_SIZE", "16777216"))  # 16MB
}

API_KEY = "asdfasdfawsreger23423rdfasdfa"
WHATSAPP_API_URL = "https://api.whatsapp.com/send"
MEDIA_UPLOAD_PATH = "media/uploads/"
TEMP_MEDIA_PATH = "media/temp/"
LOGGING_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Add any other configuration settings as needed.