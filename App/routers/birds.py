from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from fastapi_jwt_auth import AuthJWT
from App.database import get_db
from .. import schemas, models


router = APIRouter(tags=['Birds'], prefix="/bird")

@router.delete('/{id}')
def bird_delete_id(id, Authorize:AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()
    db.query(models.Bird).filter(models.Bird.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Birds deleteds': id}
    

@router.get('/')
async def get_all_bird(db: Session = Depends(get_db)):
    """_summary_
       Get a json with all bird 
    """
    bird = db.query(models.Bird).all()
    return bird


@router.get('/{id}')
async def get_one_bird(id, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one bird 
    """
    bird = db.query(models.Bird).filter(models.Bird.id == id).first()
    if not bird:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='bird not found')
    return bird


@router.put('/{id}')
def update_bird(id, request : schemas.Bird, db: Session = Depends(get_db)):
    """_summary_
       Update a json with one bird 
    """
    bird = db.query(models.Bird).filter(models.Bird.id == id)
    if not bird.first():
        pass
    bird.update(request.dict())
    db.commit()    
    return {'bird updated'}


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_bird(request : schemas.Bird, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one bird 
    """
    new_bird = models.Bird(title=request.title, text=request.text, taille=request.taille, poids=request.poids, ordre=request.ordre, localisation=request.localisation,
                           image=request.image,genre=request.genre, famille=request.famille, disparation=request.disparition, descripteur=request.descripteur)
    db.add(new_bird)
    db.commit()
    db.refresh(new_bird)
    return request
