from tokenize import Token
from fastapi import APIRouter, status, HTTPException

from sqlalchemy.orm import Session, joinedload
from fastapi.params import Depends
from App.database import get_db
from .. import schemas, models
from App.schemas import TokenData
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
load_dotenv(override=True)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter(tags=['Login'], prefix="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def generate_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/', response_model=schemas.DisplayUsers ,status_code=status.HTTP_201_CREATED)
def add_user(request : schemas.Users, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one user 
    """
    hashed_password = pwd_context.hash(request.hashed_password)
    new_User = models.Users(first_name=request.first_name, last_name=request.last_name, username=request.username, 
                            email=request.email, hashed_password=hashed_password, password_lost=request.password_lost, admin=request.admin)
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User



@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Email not found / invalid user')
    if not pwd_context.verify(request.hashed_password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password ')
    ACCESS_TOKEN = generate_token(data={"sub": user.email})
    return {"access token" : ACCESS_TOKEN, "token_type" : "bearer"}

    
def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        
    except JWTError:
        raise credentials_exception
    return token_data
    