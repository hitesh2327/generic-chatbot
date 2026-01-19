from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

from app.core.database import Base
import app.models  # 👈 VERY IMPORTANT (loads ALL models)

# Alembic Config
config = context.config

# Set DB URL from env
config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL")
)

# Logging
fileConfig(config.config_file_name)

target_metadata = Base.metadata

context.configure(
    url=config.get_main_option("sqlalchemy.url"), # uncomment if you are using offline
    target_metadata=target_metadata,
    # literal_binds=True,
    include_schemas=True,  # 👈 REQUIRED - 🚨 If include_schemas=True is missing → schemas will break.
    compare_type=True
)
