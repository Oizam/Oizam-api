from fastapi import APIRouter, status, HTTPException, Request
from App.routers.login import get_current_user
from sqlalchemy.orm import Session, joinedload
from fastapi.params import Depends
from tensorflow import keras
from App.database import get_db
from .. import schemas, models

bird_dex = pd.read_csv("/code/app/dict_liste_oiseaux.csv")
model = keras.models.load_model('App/data/model.h5')

router = APIRouter(tags=['predict'], prefix="/predict")


@router.get('/')
async def get_prediction(request : Request):
    
    mat = await request.json()
    mat = eval(mat)
    predict = model.predict(mat['Image'])
    predict = predict.argmax() + 1

    return({"result" : bird_dex[bird_dex['number'] == predict]["name"].values[0]})