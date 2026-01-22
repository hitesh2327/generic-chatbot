from pydantic import BaseModel
from decimal import Decimal

class PlanResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    billing_cycle: str
    is_popular: bool

    class Config:
        from_attributes = True
