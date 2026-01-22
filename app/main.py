from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from .api.chat import router as chat_router
from .api.auth import router as auth_router
from .api.chat_ws import router as chat_ws_router
from .api.pricing import router as pricing_router

app = FastAPI(title="Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",  # optional
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/api")
app.include_router(chat_ws_router)
app.include_router(pricing_router)

