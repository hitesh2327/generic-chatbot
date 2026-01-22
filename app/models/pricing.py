from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, func
from app.core.database import Base

class Plan(Base):
    __tablename__ = "plans"
    __table_args__ = {"schema": "admin"}  # 👈 IMPORTANT

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    monthly_price = Column(Numeric(10, 2), nullable=False)
    yearly_price = Column(Numeric(10, 2), nullable=False)
    is_popular = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
