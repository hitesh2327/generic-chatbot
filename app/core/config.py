from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Chatbot API"

settings = Settings()
