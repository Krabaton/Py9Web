"""
Session Async
"""
import asyncio

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=False)
AsyncDBSession = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_email = Column('email', String(150), nullable=False, index=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    user = relationship(User)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await init_models()
    async with AsyncDBSession() as session:
        new_user = User(fullname='Mykola Gryshyn')
        session.add(new_user)
        new_address = Address(user_email="mykola@i.ua", user=new_user)
        session.add(new_address)
        await session.commit()

        new_user = User(fullname='Denys Tantsiura')
        session.add(new_user)
        new_address = Address(user_email="denis@meta.ua", user=new_user)
        session.add(new_address)
        await session.commit()

        u = await session.execute(select(User))
        r_u = u.scalars().all()
        for u in r_u:
            print(u.id, u.fullname)

        adrs = await session.execute(select(Address).join(Address.user))
        addresses = adrs.scalars().all()
        print(adrs)
        for a in addresses:
            print(a.id, a.user_email, a.user.fullname)

        await session.close()

if __name__ == '__main__':
    asyncio.run(main())
