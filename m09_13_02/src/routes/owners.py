from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import owners as repository_owners
from src.schemas import OwnerResponse, OwnerModel


router = APIRouter(prefix="/owners", tags=['owners'])


@router.get("/", response_model=List[OwnerResponse], name="Повернути власників")
async def get_owners(db: Session = Depends(get_db)):
    owners = await repository_owners.get_owners(db)
    return owners


@router.get("/{owner_id}", response_model=OwnerResponse)
async def get_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = await repository_owners.get_owner_by_id(owner_id, db)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return owner


@router.post("/", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
async def create_owner(body: OwnerModel, db: Session = Depends(get_db)):
    owner = await repository_owners.get_owner_by_email(body.email, db)
    if owner:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')

    owner = await repository_owners.create(body, db)
    return owner


@router.put("/{owner_id}", response_model=OwnerResponse)
async def update_owner(body: OwnerModel, owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = await repository_owners.update(owner_id, body, db)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return owner


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = await repository_owners.remove(owner_id, db)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return owner
