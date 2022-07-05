from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session, joinedload
from fastapi.params import Depends
from fastapi_jwt_auth import AuthJWT
from App.database import get_db
from .. import schemas, models


router = APIRouter(tags=['OiseauxDex'], prefix="/OiseauxDex")

@router.get('/')
async def get_all_bird(db: Session = Depends(get_db)):
    """_summary_
       Get a json with all bird 
    """
    birds_users = db.query(models.birds_users).all()
    return birds_users


@router.get('/{id}')
async def get_one_user(id, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one user 
    """
    birds_users = db.query(models.Users).options(joinedload(models.Users.birds)).filter(models.Users.id == id).all()
    if not birds_users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found')
    return birds_users

@router.post('/',status_code=status.HTTP_201_CREATED)
def add_user(request : schemas.birds_users, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one user 
    """
    new_oiseaux_dex = models.birds_users(bird_id=request.bird_id, user_id=request.user_id)
    db.add(new_oiseaux_dex)
    db.commit()
    db.refresh(new_oiseaux_dex)
    return {"add" : "nouveaux oiseaux ajouter"}