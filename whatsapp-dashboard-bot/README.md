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

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.