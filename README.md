# Attack Capital AI - Real-time Chat Application

A modern real-time chat application built with React, FastAPI, and LiveKit, featuring AI-powered responses using Google's Gemini AI.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   LiveKit       │
│   (React/Vite)  │◄──►│   (FastAPI)     │◄──►│   Server        │
│   Port: 5173    │    │   Port: 3001    │    │   (External)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Components │    │   AI Agent      │    │   Real-time     │
│   - ChatWindow  │    │   - Gemini AI   │    │   Communication │
│   - MessageInput│    │   - Memory      │    │   - WebRTC      │
│   - LiveKit     │    │   - SQLite/     │    │   - Data Channel│
│   Integration   │    │     Mem0        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Features

- **Real-time Chat**: WebRTC-based communication via LiveKit
- **AI-Powered Responses**: Google Gemini AI integration for intelligent replies
- **Memory System**: Conversation context with SQLite or Mem0 backend
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **Responsive Design**: Mobile-friendly interface with shadcn/ui components
- **Docker Support**: Containerized backend for easy deployment
- **Health Monitoring**: Built-in health checks and status endpoints

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **Docker** (optional, for containerized deployment)
- **LiveKit Server** (self-hosted or cloud instance)
- **Google AI API Key** (for Gemini AI responses)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd attack-capital-ai
```

### 2. Backend Setup

#### Option A: Local Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your actual credentials
```

#### Option B: Docker Deployment

```bash
cd backend

# Build the Docker image
docker build -t attack-capital-backend .

# Run with environment variables
docker run -p 3001:3001 \
  -e LIVEKIT_API_KEY=your_api_key \
  -e LIVEKIT_API_SECRET=your_api_secret \
  -e LIVEKIT_WS_URL=wss://your-livekit-server.com \
  -e GEMINI_API_KEY=your_gemini_key \
  attack-capital-backend
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables (optional)
# Create .env.local with:
# VITE_BACKEND_URL=http://localhost:3001
# VITE_AGENT_IDENTITY=assistant

# Start development server
npm run dev
```

## ⚙️ Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# LiveKit Configuration (Required)
LIVEKIT_API_KEY=your_livekit_api_key_here
LIVEKIT_API_SECRET=your_livekit_api_secret_here
LIVEKIT_WS_URL=wss://your-livekit-server.com

# Gemini AI Configuration (Optional)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Agent Configuration
AGENT_IDENTITY=assistant

# CORS Configuration
CORS_ORIGINS=http://localhost:8080,http://localhost:3000,http://localhost:5173

# Optional: Mem0 Configuration
MEM0_BASE_URL=https://api.mem0.ai
MEM0_API_KEY=your_mem0_api_key
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
VITE_BACKEND_URL=http://localhost:3001
VITE_AGENT_IDENTITY=assistant
```

## 🏃‍♂️ Running the Application

### Option 1: Local Development (No Docker)

#### Prerequisites
- Python 3.11+ installed
- Virtual environment activated
- Environment variables configured

#### Backend Setup & Run

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env with your actual credentials
   # Required: LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_WS_URL
   # Optional: GEMINI_API_KEY for AI responses
   ```

5. **Start the backend server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 3001
   ```

#### Frontend Setup & Run

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

#### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:3001
- **Health Check**: http://localhost:3001/health
- **API Documentation**: http://localhost:3001/docs (FastAPI auto-generated docs)

### Option 2: Docker Deployment

#### Backend Only with Docker

```bash
# Build the Docker image
docker build -t attack-capital-backend ./backend

# Run with environment variables
docker run -p 3001:3001 \
  -e LIVEKIT_API_KEY=your_api_key \
  -e LIVEKIT_API_SECRET=your_api_secret \
  -e LIVEKIT_WS_URL=wss://your-livekit-server.com \
  -e GEMINI_API_KEY=your_gemini_key \
  attack-capital-backend
```

#### Using Environment File with Docker

```bash
# Create .env file in backend directory first
cp backend/env.example backend/.env
# Edit backend/.env with your credentials

# Run with environment file
docker run -p 3001:3001 --env-file ./backend/.env attack-capital-backend
```

### Production Mode

#### Local Production

1. **Build Frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Run Backend** (without reload for production):
   ```bash
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 3001
   ```

#### Docker Production

```bash
# Build and run in production mode
docker run -p 3001:3001 \
  --env-file ./backend/.env \
  --restart unless-stopped \
  attack-capital-backend
```

## 📁 Project Structure

```
attack-capital-ai/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── agents/            # AI Agent Logic
│   │   │   └── chat_agent.py
│   │   ├── routes/            # API Routes
│   │   │   ├── agent.py       # Agent endpoints
│   │   │   └── token.py       # LiveKit token generation
│   │   ├── services/          # Business Logic
│   │   │   ├── livekit_token.py
│   │   │   ├── llm_client.py  # Gemini AI integration
│   │   │   └── memory_store.py # Memory management
│   │   ├── utils/             # Utilities
│   │   │   └── config.py      # Configuration management
│   │   └── main.py            # FastAPI application
│   ├── tests/                 # Backend tests
│   ├── Dockerfile             # Docker configuration
│   ├── requirements.txt       # Python dependencies
│   └── env.example           # Environment variables template
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React Components
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── ui/            # shadcn/ui components
│   │   ├── hooks/             # Custom React Hooks
│   │   │   └── useLivekitChat.ts
│   │   ├── pages/             # Page Components
│   │   │   ├── Chat.tsx
│   │   │   ├── Login.tsx
│   │   │   └── MinimalLivekitTest.tsx
│   │   ├── lib/               # Utilities
│   │   └── App.tsx            # Main App component
│   ├── package.json           # Node.js dependencies
│   └── vite.config.ts         # Vite configuration
└── README.md                  # This file
```

## 🔌 API Endpoints

### Backend API (Port 3001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check endpoint |
| GET | `/token` | Generate LiveKit access token |
| POST | `/agent/reply` | Get AI response for user message |
| GET | `/agent/status` | Check agent configuration status |

### Example API Usage

```bash
# Health check
curl http://localhost:3001/health

# Get LiveKit token
curl "http://localhost:3001/token?identity=user1&room=default"

# Send message to AI agent
curl -X POST http://localhost:3001/agent/reply \
  -H "Content-Type: application/json" \
  -d '{"userId": "user1", "text": "Hello!"}'
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🐳 Docker Deployment

### Backend Only

```bash
# Build image
docker build -t attack-capital-backend ./backend

# Run container
docker run -p 3001:3001 \
  --env-file ./backend/.env \
  attack-capital-backend
```

### Full Stack with Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "3001:3001"
    environment:
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
      - LIVEKIT_WS_URL=${LIVEKIT_WS_URL}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_BACKEND_URL=http://localhost:3001
```

## 🔧 Development

### Adding New Features

1. **Backend**: Add new routes in `backend/app/routes/`
2. **Frontend**: Add new components in `frontend/src/components/`
3. **AI Integration**: Modify `backend/app/services/llm_client.py`
4. **Memory**: Update `backend/app/services/memory_store.py`

### Code Style

- **Backend**: Follow PEP 8, use type hints
- **Frontend**: Use TypeScript, follow React best practices
- **Commits**: Use conventional commit messages

## 🚨 Troubleshooting

### Common Issues

1. **LiveKit Connection Failed**:
   - Check `LIVEKIT_WS_URL` is correct
   - Verify API key and secret
   - Ensure LiveKit server is running

2. **AI Responses Not Working**:
   - Verify `GEMINI_API_KEY` is set
   - Check API quota and billing
   - Review backend logs for errors

3. **CORS Issues**:
   - Update `CORS_ORIGINS` in backend config
   - Ensure frontend URL is included

4. **Docker Issues**:
   - Check environment variables are passed
   - Verify port mappings
   - Review container logs

### Debug Mode

```bash
# Backend with debug logging
cd backend
uvicorn app.main:app --reload --log-level debug

# Frontend with verbose output
cd frontend
npm run dev -- --debug
```

## 📚 Dependencies

### Backend Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **LiveKit API**: Real-time communication
- **Google Generative AI**: AI responses
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation

### Frontend Dependencies

- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **shadcn/ui**: Component library
- **LiveKit Client**: Real-time communication
- **Axios**: HTTP client

**Happy Chatting! 🚀**
