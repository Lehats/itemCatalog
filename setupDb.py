#!/usr/bin/env python3

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    username = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    password_hash = Column(String(64))

    def hashThePassword(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'username'         : self.name,
           'id'           : self.id,
       }


class Categories(Base):
    __tablename__ = 'categories'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }

class Parts(Base): 
    __tablename__ = 'parts' 

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(1000))
    category_id = Column(Integer,ForeignKey('categories.id'))
    category = relationship(Categories)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'description'         : self.description,
           'category'       :self.category.name,
           'creator'        :self.user.username
       }




engine = create_engine('sqlite:///parts.db')

Base.metadata.create_all(engine)