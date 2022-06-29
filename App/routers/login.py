from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from App.database import get_db
from App import schemas, models
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT

router = APIRouter(tags=['Login'], prefix="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/signup', response_model=schemas.DisplayUsers ,status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.Users, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one user 
    """
    user = db.query(models.Users).filter(models.Users.email == request.email).first()
    
    if user:
        print(user)
        print("user exist deja")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email existing already') 
    
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


    