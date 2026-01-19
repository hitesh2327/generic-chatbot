from app.core.database import engine, Base
from app.models import user, chat_message

def init_db():
    Base.metadata.create_all(bind=engine)
