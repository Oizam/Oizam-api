from tokenize import Token
from fastapi import APIRouter, status, HTTPException

from sqlalchemy.orm import Session, joinedload
from fastapi.params import Depends
from App.database import get_db
from App import schemas, models
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT
load_dotenv(override=True)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter(tags=['Login'], prefix="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/signup', response_model=schemas.DisplayUsers ,status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.Users, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one user 
    """
    # hashed_password = pwd_context.hash(request.hashed_password)
    new_User = models.Users(first_name=request.first_name, last_name=request.last_name, username=request.username, 
                            email=request.email, hashed_password=request.hashed_password, password_lost=request.password_lost, admin=request.admin)
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User



@router.post('/login')
def login(user: schemas.UserLogin, Authorize:AuthJWT=Depends(), db: Session = Depends(get_db)):
    user_connected = db.query(models.Users).filter(models.Users.email == user.email).first()
    if (user_connected.email==user.email) and (user_connected.hashed_password==user.hashed_password):
        access_token= Authorize.create_access_token(subject=user.email)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        return {"access token" : access_token, "refresh_token" : refresh_token}    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email not found / invalid user')



    
# def get_current_user(token:str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid auth credentials",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get('sub')
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
        
#     except JWTError:
#         raise credentials_exception
#     return token_data
    