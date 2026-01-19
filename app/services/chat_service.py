from typing import Dict, List
from openai import OpenAI
import os
from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
from app.models.user import User
from openai import OpenAI
# from app.services.chat_service import (
#     save_message,
#     get_chat_history,
#     build_llm_messages
# )
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history: Dict[str, List[dict]] = {}

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful, concise chatbot."
}

def get_bot_reply(db, user, message: str) -> str:
    # save user message
    save_message(db, user.id, "user", message)

    history = get_chat_history(db, user.id)

    llm_messages = [SYSTEM_PROMPT] + build_llm_messages(history)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=llm_messages,
        temperature=0.7
    )

    reply = response.choices[0].message.content

    # save assistant reply
    save_message(db, user.id, "assistant", reply)

    return reply

def save_message(db: Session, user_id: int, role: str, content: str):
    msg = ChatMessage(
        user_id=user_id,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()

def get_chat_history(db: Session, user_id: int, limit: int = 20):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.created_at.asc())
        .limit(limit)
        .all()
    )

def build_llm_messages(db_messages):
    messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in db_messages
    ]
    return messages

