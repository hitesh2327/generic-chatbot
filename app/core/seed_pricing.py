from sqlalchemy.orm import Session
from app.models.pricing import Plan

def seed_pricing(db: Session):
    if db.query(Plan).count() > 0:
        return

    plans = [
        Plan(
            name="Free",
            description="For individuals getting started",
            monthly_price=0,
            yearly_price=0,
        ),
        Plan(
            name="Pro",
            description="For professionals and growing teams",
            monthly_price=20,
            yearly_price=200,  # 2 months free
            is_popular=True,
        ),
        Plan(
            name="Business",
            description="For businesses scaling conversations",
            monthly_price=120,
            yearly_price=1200,
        ),
    ]

    db.add_all(plans)
    db.commit()
