import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel


from auth import create_access_token, get_current_user, Hash
from db import User, get_db

app = FastAPI()
hash_handler = Hash()


class UserModel(BaseModel):
    username: str
    password: str


@app.post("/signup")
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = db.query(User).filter(User.email == body.username).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    new_user = User(email=body.username, password=hash_handler.get_password_hash(body.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.email}


@app.post("/login")
async def login(body: UserModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": 'secret router', "owner": current_user.email}


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
