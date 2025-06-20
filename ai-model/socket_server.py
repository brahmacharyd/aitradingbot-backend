import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import socketio
from fastapi import FastAPI
from signal_generator import main as generate_signals

# Create the Socket.IO server with ASGI support
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'  # Allow all origins (you can restrict to frontend domain)
)

# FastAPI app for health check
app = FastAPI()

# Combine FastAPI and Socket.IO into an ASGI application
app_sio = socketio.ASGIApp(sio, other_asgi_app=app)

@app.get("/")
async def root():
    return {"message": "🧠 AI Trading Signal Server is running!"}

@sio.event
async def connect(sid, environ):
    print(f"✅ Client connected: {sid}")
    
    # Call your signal generator
    signals = generate_signals()

    if signals:
        print(f"📤 Emitting {len(signals)} signals")
        for signal in signals:
            await sio.emit('signal', signal, to=sid)
    else:
        print("⚠️ No signals to emit")

@sio.event
def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")
