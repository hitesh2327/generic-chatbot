from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from app.schema.chat import ChatRequest, ChatResponse
from app.core.dependencies import get_db, get_current_user
from app.services.chat_service import get_bot_reply, get_chat_history
from app.services.user_service import get_user_by_username
from app.services.chatbot_stream_service import stream_bot_reply

router = APIRouter(tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    user = get_user_by_username(db, username)
    reply = get_bot_reply(db, user, request.message)

    return ChatResponse(reply=reply)

@router.get("/chat/history")
def chat_history(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    user = get_user_by_username(db, username)
    messages = get_chat_history(db, user.id, limit=50)

    return [
        {
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at
        }
        for m in messages
    ]

@router.post("/chat/stream")
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    user = get_user_by_username(db, username)

    generator = stream_bot_reply(db, user, request.message)

    return StreamingResponse(
        generator,
        media_type="text/event-stream"
    )