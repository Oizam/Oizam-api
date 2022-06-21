from fastapi import APIRouter, status, HTTPException

from sqlalchemy.orm import Session, joinedload
from fastapi.params import Depends
from App.database import get_db
from .. import schemas, models
from passlib.context import CryptContext

router = APIRouter(tags=['Users'], prefix="/user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.delete('/{id}')
def bird_delete(id, db: Session = Depends(get_db)):
    db.query(models.Users).filter(models.Users.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Users Deleted'}

@router.get('/')
async def get_all_user(db: Session = Depends(get_db)):
    """_summary_
       Get a json with all user 
    """
    users = db.query(models.Users).all()
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found')
    return users


@router.get('/{id}}')
async def get_one_user(id, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one user 
    """
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

@router.get('/get_user_view/{id}}', response_model=schemas.UserSchema)
async def get_one_user_view(id, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one user 
    """
    user = db.query(models.Users).options(joinedload(models.Users.birds)).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.put('/{id}')
def update_user(id, request : schemas.Users, db: Session = Depends(get_db)):
    """_summary_
       Update a json with one user 
    """
    user = db.query(models.Users).filter(models.Users.id == id)
    if not user.first():
        pass
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='bird not found')
    user.update(request.dict())
    db.commit()    
    return {'bird updated'}


@router.post('/', response_model=schemas.DisplayUsers ,status_code=status.HTTP_201_CREATED)
def add_user(request : schemas.Users, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one user 
    """
    hashed_password = pwd_context.hash(request.hashed_password)
    new_User = models.Users(first_name=request.first_name, last_name=request.last_name, username=request.username, email=request.email, hashed_password=hashed_password, password_lost=request.password_lost,
                           admin=request.admin)
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User

