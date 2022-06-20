from dataclasses import Field
import logging as lg
from pydantic import BaseModel, Field
from typing import List, Optional

class Bird(BaseModel):
    lg.info('Class Bird')
    id : int
    class_bird : str
    french_name : str
    english_name : str
    title : str = Field(example="Pigeon")
    text : str = Field(example="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
    taille : str = Field(example= " : 15 cm")
    poids : str = Field(example= " : 15 cm")
    ordre : str = Field(example="200g a 300g")
    localisation : str = Field(example='https://www.oiseaux.net/maps/images/accenteur.a.gorge.noire.1.200.w.png')
    image : str = Field(example="https://www.oiseaux.net/photos/john.gould/images/accenteur.a.gorge.noire.jogo.0p.jpg")
    genre : str = Field(example="On ne sait pas")
    famille : str = Field(example="famille ")
    disparition : str = Field(example='LC')
    descripteur : str = Field(example="Gmelin, JF, 1789")
    envergure: str = Field(example="30 cm.")  
    espece: str = Field(example="bonariensis")
    
class Users(BaseModel):
    lg.info('Class Users')
    first_name : str = Field(example="Guillaume")
    last_name : str = Field(example="SOULAT")
    username : str = Field(example="Berry")
    email : str = Field(example="gsoulat31@gmail.com")
    hashed_password : str = Field(example="devine")
    password_lost : str = Field(example="Oh tu as perdu ton mot de passe ? c'est pas grave")
    admin : bool = False  
    
class Login(BaseModel): 
    email : str = Field(example="oizam@gmail.com")
    password : str = Field(example="password") 

class DisplayUsers(BaseModel):
    first_name : str 
    last_name : str
    username : str
    email : str
    
    class Config:
        orm_mode = True
        
class BirdSchema(Bird):
    users : List[DisplayUsers]
    
class UserSchema(DisplayUsers):
    birds : List[Bird]
    
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
    
class TokenData(BaseModel):
    email : str | None = None
    
class UserInDB(Users):
    hashed_password: str