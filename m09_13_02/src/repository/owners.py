from sqlalchemy.orm import Session

from src.database.models import Owner
from src.schemas import OwnerModel


async def get_owners(db: Session):
    owners = db.query(Owner).all()
    return owners


async def get_owner_by_id(owner_id: int, db: Session):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    return owner


async def get_owner_by_email(email: str, db: Session):
    owner = db.query(Owner).filter_by(email=email).first()
    return owner


async def create(body: OwnerModel, db: Session):
    owner = Owner(**body.dict())
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


async def update(owner_id: int, body: OwnerModel, db: Session):
    owner = await get_owner_by_id(owner_id, db)
    if owner:
        owner.email = body.email
        db.commit()
    return owner


async def remove(owner_id: int, db: Session):
    owner = await get_owner_by_id(owner_id, db)
    if owner:
        db.delete(owner)
        db.commit()
    return owner
