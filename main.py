from fastapi import FastAPI, Request
from App import models
from App.database import engine, get_db
from App.routers import birds, users, login, predict
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
import pandas as pd
import logging as lg
import uvicorn
import os

app = FastAPI(
    title="Oizam API",
    description="Get details for all the birds on our website",
    terms_of_service="oizam.com/terms_of_service",
    contact={
        "Team Developer" : "Charly, Guillaume, Mickael, Valentin and Yanis ",
        "Website" : "wwww.oizam.com",
        "email" : "oizam@oizam.com",
    },
    license_info={
        "name": "Open Simplon"
    }
)


templates = Jinja2Templates(directory="App/templates")


@app.get('/' , response_class=HTMLResponse)
async def depart(request: Request):
    """_summary_
       Get a json with all bird 
    """
    return templates.TemplateResponse("index.html", {'some_object':"some_object", 'request':request})


@app.get('/coco')
def home():
    return({"Bienvenue" : "bienvenue"})

app.include_router(birds.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(predict.router)

# def init_db():
lg.info('Database destoy')
models.Base.metadata.drop_all(engine)
lg.info('Database created!')
models.Base.metadata.create_all(engine)

lg.info('Database import bird')
data = pd.read_csv ('App\data\OiseauxFini.csv')   
df = pd.DataFrame(data)
df.to_sql('birds', con = engine, if_exists='append', index=False)

lg.info('Database import users!')
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# for i in range(1,11):
#     hashed_password = pwd_context.hash("123")
#     new_User = models.Users(first_name='toto' + str(i), last_name='toto' + str(i), username='toto' + str(i), email='toto' + str(i) + "@gmail.com", hashed_password=hashed_password, password_lost="request.password_lost",
#                         admin="True")
#     lg.info(f'Users : {new_User}')
#     db = get_db
#     db.add(new_User)
#     db.commit()
#     db.refresh(new_User)
lg.info('Database initialized!')

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))
    # init_db()





