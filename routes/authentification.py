from fastapi import FastAPI, HTTPException, Depends,APIRouter
from prisma import Prisma
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
import secrets
import string
import bcrypt



router = APIRouter()


prisma = Prisma()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verify the user's password
def verify_password(plain_password, hashed_password):
    return (bcrypt.checkpw(plain_password, hashed_password))

async def authenticate_user(username: str, password: str):
    user =  await prisma.user.find_unique(where={"username": username})
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    if not user:
        return False
    if not bcrypt.checkpw(password.encode(), hashed_password):
        return False
    del user.password
    return user


# Create an access token for the user
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta()
    to_encode.update({"exp": expire})
    alphabet = string.ascii_letters + string.digits
    encoded_jwt = ''.join(secrets.choice(to_encode,alphabet) for i in range(8))
    return encoded_jwt


@router.on_event("startup")
async def startup():
    await prisma.connect()
@router.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

    
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user