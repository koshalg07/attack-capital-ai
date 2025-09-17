
## AI Chat Agent (Frontend) – LiveKit Room Chat with Memory-Ready Hooks

Minimal React (Vite + TS + Tailwind) frontend for a LiveKit-powered chat room. Users join with a username and room name. Messages are exchanged over the LiveKit data channel. The UI is ready for an AI agent participant and a memory-augmented backend (mem0/RAG) that replies in real time.

This repo is the frontend part of the assignment. It expects a backend that:
- Issues LiveKit access tokens at `GET /token?identity={id}&room={room}`
- Joins the same LiveKit room as an AI agent and posts messages on topic `lk.chat`
- Retrieves user memory context (mem0 or similar), generates responses with an LLM, and sends them back via data channel

### Features
- Login with display name and room name (multi-room support)
- Real-time chat: send/receive messages on topic `lk.chat`
- Connection status and leave flow
- Typing indicator for assistant
- System message when the AI agent joins (configurable via `VITE_AGENT_IDENTITY`)

### Tech
- React + TypeScript + Vite
- TailwindCSS + shadcn/ui components
- LiveKit client SDK (data channel)

---

## Quickstart

1) Install
```bash
npm install
```

2) Configure environment
Create a `.env` in the project root with:
```dotenv
VITE_BACKEND_URL=http://localhost:3001
VITE_AGENT_IDENTITY=assistant
```

3) Run
```bash
npm run dev
```
Open the URL shown by Vite (usually `http://localhost:5173`).

4) Use
- On the login screen, enter a display name and a room (e.g., `default`).
- The app will request a token from your backend and join the room.
- Type messages; when your AI agent backend connects as `VITE_AGENT_IDENTITY`, a system message will indicate it joined.

---

## Expected Backend (for assignment)
Implement a Python backend (e.g., `livekit-agents`) that:
- Serves `GET /token` issuing LiveKit tokens for the given `identity` and `room`.
- Connects an AI agent participant to the same room.
- On user messages, queries a memory store (mem0 or equivalent), builds a context-aware prompt, generates a reply using an LLM (OpenAI/OpenRouter/Groq), and sends the reply on topic `lk.chat`.
- Optionally persists new memories from conversations.

> This frontend calls `${VITE_BACKEND_URL}/token` and publishes/subscribes to data messages on topic `lk.chat`.

---

## Scripts
```bash
npm run dev       # start Vite dev server
npm run build     # production build
npm run preview   # preview production build
```

---

## Environment
Variables used by the frontend:
- `VITE_BACKEND_URL`: Base URL of your backend issuing tokens and hosting the agent.
- `VITE_AGENT_IDENTITY`: The LiveKit identity of your AI agent. Used to display a system message when the agent joins.

---

## Project Structure (selected)
```
src/
  pages/
    Login.tsx         # username + room inputs; persists to localStorage
    Chat.tsx          # connects to LiveKit via hook; header/status; leave
  hooks/
    useLivekitChat.ts # token fetch, connect, send/receive, typing, agent join notice
  components/
    ChatWindow.tsx, ChatMessage.tsx, MessageInput.tsx, ui/*
```

---

## Assignment Mapping
- Users join a LiveKit room with username: Implemented (`Login.tsx`, `Chat.tsx`).
- AI agent participant communicates by text: Frontend-ready; requires backend agent.
- Memory context via mem0/RAG: Backend concern; frontend agnostic.
- Real-time seamless interaction: Implemented via LiveKit data channel.
- Docs and env: Provided here; add backend docs in backend repo.


