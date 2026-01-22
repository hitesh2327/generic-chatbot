from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.pricing_service import get_pricing
from app.schema.pricing import PlanResponse

router = APIRouter(prefix="/pricing", tags=["pricing"])

@router.get("", response_model=list[PlanResponse])
def pricing(
    billing_cycle: str = Query("monthly", regex="^(monthly|yearly)$"),
    db: Session = Depends(get_db),
):
    return get_pricing(db, billing_cycle)
