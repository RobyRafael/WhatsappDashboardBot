# WhatsApp Dashboard Bot

## Overview
The WhatsApp Dashboard Bot is a modular application designed to facilitate the sending of messages and media through WhatsApp via a bot interface. This project is built using Python with FastAPI for the backend and includes a dashboard for managing media uploads and notifications.

## Project Structure
```
whatsapp-dashboard-bot
├── src
│   ├── bot                # Contains the WhatsApp bot implementation
│   ├── api                # Contains the FastAPI application and routes
│   ├── dashboard          # Contains the dashboard application for media management
│   └── utils              # Contains utility functions for database and logging
├── media                  # Directory for storing uploaded media files
│   ├── uploads            # Directory for uploaded media
│   └── temp               # Directory for temporary media files
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration for services
├── Dockerfile.bot         # Dockerfile for the WhatsApp bot
├── Dockerfile.api         # Dockerfile for the API
├── Dockerfile.dashboard    # Dockerfile for the dashboard
└── README.md              # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/RobyRafael/whatsapp-dashboard-bot.git
   cd whatsapp-dashboard-bot
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Configuration
Before running the application, you need to set your API key:

1. **Option 1: Environment Variable**
   ```bash
   export API_KEY="your-super-secret-api-key-here"
   ```

2. **Option 2: Edit docker-compose.yml**
   Change the API_KEY value in the docker-compose.yml file

### Running the Application
To run the application using Docker, execute the following command:
```
docker-compose up --build
```

This command will build the necessary Docker images and start the services defined in `docker-compose.yml`.

### Accessing the Services
Once the application is running, you can access:

- **Dashboard**: http://localhost:5000
- **API Documentation**: http://localhost:8001/docs
- **API Health Check**: http://localhost:8001/api/health

### API Authentication
All API requests require the `X-API-Key` header with your configured API key:

```bash
curl -H "X-API-Key: your-super-secret-api-key-here" http://localhost:8001/api/health
```

### API Endpoints
- **POST /api/messages**: Send a message via WhatsApp
- **POST /api/media**: Upload and send media files
- **GET /api/health**: Health check endpoint

## WhatsApp Login Methods

### Method 1: Simple Testing (Recommended for Development)
```bash
# Menggunakan metode sederhana dari testing.py
python simple_test.py
```

### Method 2: Login Script
```bash
# Script login dengan menu lengkap
python login_whatsapp.py
```

### Method 3: Original Testing Method
```bash
# Menggunakan metode original dari testing.py
python testing.py
```

## Key Features

✅ **Simple Login Detection** - Menggunakan metode try-except yang sederhana  
✅ **QR Code Detection** - Deteksi otomatis QR code dan status login  
✅ **30 Second Wait Time** - Waktu tunggu yang cukup untuk scan QR  
✅ **Reliable Status Check** - Pengecekan status yang konsisten  
✅ **Error Handling** - Penanganan error yang baik  

## Troubleshooting

Jika ada masalah dengan deteksi login:

1. **Gunakan metode testing.py** yang sudah terbukti bekerja
2. **Tunggu 30 detik** setelah membuka WhatsApp Web
3. **Pastikan QR code di-scan** dengan benar
4. **Restart script** jika login gagal

## Usage Examples

### Basic Usage
```python
from src.bot.whatsapp_bot import WhatsAppBot
import time

# Setup bot
bot = WhatsAppBot()

# Open WhatsApp Web (like testing.py)
bot.driver.get("https://web.whatsapp.com")
time.sleep(30)  # Wait for login

# Check login status
if bot.check_login_status():
    # Send message
    result = bot.send_message("+628123456789", "Hello!")
    print(result)

bot.close()
```