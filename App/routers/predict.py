# from fastapi import APIRouter, status, HTTPException, Request
# from sqlalchemy.orm import Session, joinedload
# from fastapi.params import Depends
# from tensorflow import keras
# from App.database import get_db
# from .. import schemas, models
# import pandas as pd

# router = APIRouter(tags=['predict'], prefix="/predict")

# # model = keras.models.load_model('code/App/data/complete_modelFR.h5')

# @router.get('/')
# async def get_prediction(request : Request, db: Session = Depends(get_db)):
#     mat = await request.json()
#     mat = eval(mat)
#     # predict = model.predict(mat['Image'])
#     predict = int(predict.argmax() + 201) 
#     bird = db.query(models.Bird).filter(models.Bird.id == predict).first()
#     return(bird)

