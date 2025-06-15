import socketio
import asyncio
from fastapi import FastAPI
import uvicorn
from signal_generator import main as generate_signals

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app_sio = socketio.ASGIApp(sio, other_asgi_app=app)
@app.get("/")
async def root():
    return {"message": "🧠 AI Trading Signal Server is running!"}
@sio.event
async def connect(sid, environ):
    print(f"✅ Client connected: {sid}")
    
    signals = generate_signals()  # This should now return the list

    if signals:
        print(f"📤 Emitting {len(signals)} signals")
        for signal in signals:
            await sio.emit('signal', signal, to=sid)
    else:
        print("⚠️ No signals to emit")

@sio.event
def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")

if __name__ == "__main__":
    uvicorn.run(app_sio, host="0.0.0.0", port=3000)
