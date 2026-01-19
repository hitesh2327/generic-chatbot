from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.core.rate_limiter import rate_limit
from app.core.database import SessionLocal
from app.core.security import decode_token
from app.services.user_service import get_user_by_username
from app.services.chatbot_stream_service import stream_bot_reply

router = APIRouter()

@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()

    db: Session = SessionLocal()

    try:
        # 1️⃣ Authenticate via JWT
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008)
            return

        username = decode_token(token)
        user = get_user_by_username(db, username)

        if not user:
            await websocket.close(code=1008)
            return

        # 2️⃣ Message loop
        while True:
            key = f"rate:ws:user:{user.id}"

            if not rate_limit(key, limit=20, window_seconds=60):
                await websocket.send_text("⚠️ Rate limit exceeded")
                continue
            data = await websocket.receive_text()

            # Stream LLM tokens
            for token_chunk in stream_bot_reply(db, user, data):
                await websocket.send_text(token_chunk)

            # End of message signal
            await websocket.send_text("__END__")

    except WebSocketDisconnect:
        print("Client disconnected")

    finally:
        db.close()
