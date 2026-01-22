from sqlalchemy.orm import Session
from app.models.pricing import Plan

def get_pricing(db: Session, billing_cycle: str):
    plans = (
        db.query(Plan)
        .filter(Plan.is_active == True)
        .order_by(Plan.monthly_price.asc())
        .all()
    )

    response = []
    for plan in plans:
        price = (
            plan.monthly_price
            if billing_cycle == "monthly"
            else plan.yearly_price
        )

        response.append({
            "id": plan.id,
            "name": plan.name,
            "description": plan.description,
            "price": price,
            "billing_cycle": billing_cycle,
            "is_popular": plan.is_popular,
        })

    return response
