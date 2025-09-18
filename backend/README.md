# Attack Capital AI - Backend

FastAPI backend that mints LiveKit access tokens, provides a simple chat memory store, and wraps OpenAI for replies (with a stub fallback).

## Requirements
- Python 3.11
- (Optional) LiveKit server SDK credentials
- (Optional) OpenAI API key

## Setup
```bash
cd backend
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` (see `.env.example`):
```
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
LIVEKIT_WS_URL=wss://your-livekit-host
PORT=3001
AGENT_IDENTITY=assistant
GEMINI_API_KEY=
```

## Run
```bash
uvicorn app.main:app --reload --port 3001
```

Test the token endpoint:
```bash
curl "http://localhost:3001/token?identity=tester&room=default"
```

## Tests
```bash
pytest -q
```

## Docker
```bash
docker build -t attack-capital-backend ./backend
docker run --env-file ./backend/.env -p 3001:3001 attack-capital-backend
```

## Notes
- If `GEMINI_API_KEY` is set, Gemini will be used; otherwise a stub echo is returned.
- The LiveKit agent skeleton is provided but not auto-run.


