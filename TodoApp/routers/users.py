from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos, Users
from database import SessionLocal
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user:user_dependecy, db:db_dependecy):
    query = db.query(Users).filter(Users.id == user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return query

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependecy, db: db_dependecy, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password= bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

#@router.get('/',status_code=status.HTTP_200_OK)
#async def get_user(user:user_dependecy, db:db_dependecy):
    #if user is None:
        #raise HTTPException(status_code=401, detail='Authentication Failed')
    #return db.query(Users).filter(Users.id == user.get('id')).first()