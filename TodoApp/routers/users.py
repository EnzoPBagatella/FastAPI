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

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user:user_dependecy, db:db_dependecy):
    query = db.query(Users).filter(Users.id == user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return query
    
#@router.get('/',status_code=status.HTTP_200_OK)
#async def get_user(user:user_dependecy, db:db_dependecy):
    #if user is None:
        #raise HTTPException(status_code=401, detail='Authentication Failed')
    #return db.query(Users).filter(Users.id == user.get('id')).first()