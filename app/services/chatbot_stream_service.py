from openai import OpenAI
from sqlalchemy.orm import Session
from app.services.chat_service import save_message, get_chat_history, build_llm_messages

client = OpenAI()

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful chatbot."
}

def stream_bot_reply(db: Session, user, user_message: str):
    # save user message immediately
    save_message(db, user.id, "user", user_message)

    history = get_chat_history(db, user.id)
    messages = [SYSTEM_PROMPT] + build_llm_messages(history)

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        stream=True
    )

    full_reply = ""
    try:
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_reply += delta
                yield f"data: {delta}\n\n"  # 👈 STREAM TOKEN
    except Exception:
        yield "\n[Stream interrupted]"
        
    # save assistant reply after stream ends
    save_message(db, user.id, "assistant", full_reply)
