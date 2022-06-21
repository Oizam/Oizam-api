from fastapi import APIRouter, Request
from sqlalchemy.orm import Session, joinedload
from fastapi.params import Depends
from tensorflow import keras
from App.database import get_db
from .. import models
import pandas as pd

bird_dex = pd.read_csv("code/App/data/OiseauxFini.csv")
model = keras.models.load_model('code/App/data/model.h5')

router = APIRouter(tags=['predict'], prefix="/predict")


@router.get('/')
async def get_prediction(request : Request, db: Session = Depends(get_db)):
    
    mat = await request.json()
    mat = eval(mat)
    predict = model.predict(mat['Image'])
    predict = predict.argmax() + 1
    bird = db.query(models.Bird).filter(models.Bird.id == predict).first()

    return({"result" : bird})