from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import CatResponse, CatModel, CatVaccinatedModel
from src. repository import cats as repository_cats

router = APIRouter(prefix="/cats", tags=['cats'])


@router.get("/", response_model=List[CatResponse])
async def get_cats(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)):
    cats = await repository_cats.get_cats(limit, offset, db)
    return cats


@router.get("/{cat_id}", response_model=CatResponse)
async def get_cat(cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = await repository_cats.get_cat_by_id(cat_id, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return cat


@router.post("/", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
async def create_cat(body: CatModel, db: Session = Depends(get_db)):
    cat = await repository_cats.create(body, db)
    return cat


@router.put("/{cat_id}", response_model=CatResponse)
async def update_cat(body: CatModel, cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = await repository_cats.update(cat_id, body, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return cat


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_cat(cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = await repository_cats.remove(cat_id, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return cat


@router.patch("/{cat_id}/vaccinated", response_model=CatResponse)
async def vaccinated_cat(body: CatVaccinatedModel, cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = await repository_cats.set_vaccinated(cat_id, body, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return cat
