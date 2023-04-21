import configparser
import pathlib

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.conf.config import settings


URI = settings.sqlalchemy_database_url

engine = create_engine(URI, echo=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
