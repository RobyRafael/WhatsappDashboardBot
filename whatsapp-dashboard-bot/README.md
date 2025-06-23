# WhatsApp Dashboard Bot

![WhatsApp Bot](https://img.shields.io/badge/WhatsApp-Bot-25D366?style=for-the-badge&logo=whatsapp)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)

## 📋 Overview

WhatsApp Dashboard Bot adalah aplikasi modular yang memungkinkan pengiriman pesan dan media melalui WhatsApp Web menggunakan Selenium automation. Project ini dibangun dengan Python, FastAPI untuk backend API, dan dashboard web untuk manajemen media dan notifikasi.

**Fitur Utama:**
- 🤖 **Automated WhatsApp Web** - Bot otomatis dengan session persistent
- 📱 **Multi-Modal Messaging** - Support text dan media files
- 🌐 **RESTful API** - FastAPI dengan dokumentasi Swagger
- 📊 **Web Dashboard** - Interface untuk upload dan manage media
- 🔒 **Secure Authentication** - API key protection
- 🐳 **Docker Ready** - Containerized deployment
- 🔄 **Session Management** - Login sekali, pakai berkali-kali

## 🏗️ Project Structure

```
whatsapp-dashboard-bot/
├── 📁 src/
│   ├── 📁 bot/
│   │   ├── whatsapp_bot.py      # Core WhatsApp automation
│   │   └── config.py            # Bot configuration
│   ├── 📁 api/
│   │   └── main.py              # FastAPI application
│   └── 📁 dashboard/
│       └── app.py               # Web dashboard
├── 📁 media/
│   ├── uploads/                 # Uploaded media files
│   └── temp/                    # Temporary files
├── 📁 chrome_user_data/         # Chrome session data (auto-generated)
├── 📁 User_Data*/               # Multiple Chrome profiles
├── 🐳 docker-compose.yml        # Docker services
├── 🐳 Dockerfile.*             # Docker configurations
├── 📄 requirements.txt         # Python dependencies
├── 🧪 testing.py               # Manual testing script
├── 🧪 testing_send_message.py  # Interactive testing
├── 🔑 login_whatsapp.py        # Login helper script
└── 📖 README.md                # Documentation
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Google Chrome** (latest version)
- **ChromeDriver** (auto-managed by Selenium)
- **Docker & Docker Compose** (optional)

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/RobyRafael/whatsapp-dashboard-bot.git
   cd whatsapp-dashboard-bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment**
   ```bash
   # Windows
   set API_KEY=your-super-secret-api-key-here
   set HEADLESS=false
   
   # Linux/Mac
   export API_KEY="your-super-secret-api-key-here"
   export HEADLESS="false"
   ```

### 🔧 Configuration

Edit environment variables in `docker-compose.yml` or set them locally:

```yaml
environment:
  - API_KEY=your-super-secret-api-key-here
  - HEADLESS=false  # Set to true for production
```

## 📱 WhatsApp Login Methods

### Method 1: Interactive Testing (Recommended for Development)
```bash
python testing_send_message.py
```
**Features:**
- ✅ Interactive menu system
- ✅ Visual browser (non-headless)
- ✅ Step-by-step debugging
- ✅ Real-time element inspection

### Method 2: Simple Login Script
```bash
python login_whatsapp.py
```
**Features:**
- ✅ Clean login interface
- ✅ Session persistence
- ✅ QR code guidance

### Method 3: Original Testing
```bash
python testing.py
```
**Features:**
- ✅ Basic functionality test
- ✅ Login validation

## 🐳 Docker Deployment

### Development Mode (with GUI)
```bash
# Set environment for visible browser
echo "HEADLESS=false" > .env
docker-compose up --build
```

### Production Mode (headless)
```bash
# Set environment for headless browser
echo "HEADLESS=true" > .env
docker-compose up --build -d
```

### Services
- **API Service**: http://localhost:8000
- **Dashboard**: http://localhost:5000

## 🌐 API Documentation

### Authentication
All API requests require the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-api-key-here" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/health
```

### Endpoints

#### 📤 Send Text Message
```bash
POST /api/messages
```

**Request:**
```json
{
  "phone_number": "+628123456789",
  "message": "Hello from WhatsApp Bot!"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Pesan berhasil dikirim",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 📎 Send Media File
```bash
POST /api/media
```

**Request (multipart/form-data):**
- `file`: Media file (image, video, document)
- `phone_number`: Target phone number
- `caption`: Optional caption

#### 🔍 Health Check
```bash
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "bot_status": "available",
  "login_status": "logged_in",
  "session_info": {
    "user_data_dir": "chrome_user_data",
    "profile": "WhatsApp",
    "headless": false
  }
}
```

#### 🔍 Login Status
```bash
GET /api/login-status
```

#### 🛠️ Debug Information
```bash
POST /api/debug
```

### 📖 Interactive API Documentation
Visit: http://localhost:8000/docs

## 💻 Local Development

### 1. Setup Local Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Run API server
cd src
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Run dashboard (separate terminal)
cd dashboard
python app.py
```

### 2. Testing WhatsApp Integration
```bash
# Interactive testing with visual browser
python testing_send_message.py

# Quick login test
python login_whatsapp.py
```

## 🔧 Usage Examples

### Basic Bot Usage
```python
from src.bot.whatsapp_bot import WhatsAppBot
import os

# Set environment for visible browser
os.environ["HEADLESS"] = "false"

# Initialize bot
bot = WhatsAppBot()

# Login (browser will open)
if bot.login():
    print("✅ Login successful!")
    
    # Send message
    result = bot.send_message("+628123456789", "Hello World!")
    print(result)
    
    # Send media
    result = bot.send_media("+628123456789", "path/to/image.jpg", "Caption text")
    print(result)

# Close bot
bot.close()
```

### API Client Example
```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "your-api-key-here"
headers = {"X-API-Key": API_KEY}

# Send message
response = requests.post(
    f"{API_URL}/api/messages",
    json={
        "phone_number": "+628123456789",
        "message": "Hello from API!"
    },
    headers=headers
)
print(response.json())

# Upload and send media
with open("image.jpg", "rb") as f:
    files = {"file": f}
    data = {
        "phone_number": "+628123456789",
        "caption": "Image caption"
    }
    response = requests.post(
        f"{API_URL}/api/media",
        files=files,
        data=data,
        headers=headers
    )
print(response.json())
```

## 🔍 Troubleshooting

### Login Issues
1. **QR Code tidak muncul**
   ```bash
   # Gunakan mode visible browser
   set HEADLESS=false
   python login_whatsapp.py
   ```

2. **Session expired**
   ```bash
   # Hapus session data
   rmdir /s chrome_user_data
   python login_whatsapp.py
   ```

3. **Element not found**
   ```bash
   # Debug page elements
   python testing_send_message.py
   # Pilih menu "2. Debug halaman"
   ```

### API Issues
1. **Bot not available**
   - Pastikan WhatsApp Web sudah login
   - Restart container: `docker-compose restart api`

2. **Message sending failed**
   - Cek nomor telepon format (+628xxx)
   - Pastikan kontak sudah ada di WhatsApp
   - Gunakan debug endpoint: `POST /api/debug`

### Browser Issues
1. **Chrome not found**
   ```bash
   # Install Chrome atau update PATH
   # Windows: Download dari google.com/chrome
   ```

2. **ChromeDriver issues**
   ```bash
   # Update Selenium
   pip install --upgrade selenium
   ```

## 🔐 Security

### API Key Management
- Gunakan API key yang kuat (minimal 32 karakter)
- Jangan commit API key ke repository
- Gunakan environment variables

### Session Security
- Session WhatsApp disimpan di `chrome_user_data/`
- Backup session untuk production
- Rotate session secara berkala

## 📊 Monitoring

### Logs
```bash
# Docker logs
docker-compose logs -f api

# Local logs
python -m uvicorn api.main:app --log-level info
```

### Health Monitoring
```bash
# Check API health
curl -H "X-API-Key: your-key" http://localhost:8000/api/health

# Check login status
curl -H "X-API-Key: your-key" http://localhost:8000/api/login-status
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## ⚖️ Legal Notice

This project is for educational and personal use only. Please ensure compliance with:
- WhatsApp Terms of Service
- Local regulations regarding automated messaging
- Privacy laws and consent requirements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [WhatsApp Web](https://web.whatsapp.com/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**📞 Support**: Create an issue on GitHub for questions and bug reports.

**⭐ Star this repo** if you find it helpful!