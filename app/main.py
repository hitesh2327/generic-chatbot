from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from .api.chat import router as chat_router
from .api.auth import router as auth_router
from .api.chat_ws import router as chat_ws_router

app = FastAPI(title="Chatbot API")

app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/api")
app.include_router(chat_ws_router)
