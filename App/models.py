from enum import unique
import logging as lg
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from App.database import Base
from sqlalchemy.orm import relationship



class Bird(Base):
    lg.info('Class Bird')
    __tablename__ = 'birds'
    id = Column(Integer, primary_key=True, index=True)
    class_bird = Column(String)
    french_name = Column(String)
    english_name = Column(String)
    title = Column(String)    
    text = Column(String)    
    taille = Column(String)    
    poids = Column(String)    
    ordre = Column(String)    
    localisation = Column(String)    
    image = Column(String)    
    genre = Column(String)    
    famille = Column(String)    
    disparition = Column(String)    
    descripteur = Column(String)
    envergure = Column(String)    
    espece = Column(String)
    users = relationship("Users", secondary="birds_users", back_populates="birds")   
    
class Users(Base):
    lg.info('Class Users')
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    password_lost = Column(String)
    admin = Column(String)
    birds = relationship("Bird", secondary="birds_users", back_populates="users")   
    
class birds_users(Base):
    lg.info('Class Users')
    __tablename__ = 'birds_users'
    bird_id = Column(Integer, ForeignKey('birds.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    

    