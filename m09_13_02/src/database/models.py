import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, event, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    age = Column(Integer)
    vaccinated = Column(Boolean, default=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    owner = relationship("Owner", backref="cats")


@event.listens_for(Cat, 'before_insert')
def updated_vaccinated(mapper, conn, target):
    if target.nickname == 'Boris':
        target.vaccinated = True


@event.listens_for(Cat, 'before_update')
def updated_vaccinated(mapper, conn, target):
    if target.nickname == 'Boris':
        target.vaccinated = True


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    roles = Column('roles', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
