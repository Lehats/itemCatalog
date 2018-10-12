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


class Categories(Base):
    __tablename__ = 'categories'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class Parts(Base): 
    __tablename__ = 'parts' 

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(1000))
    category_id = Column(Integer,ForeignKey('categories.id'))
    category = relationship(Categories)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)




engine = create_engine('sqlite:///parts.db')

Base.metadata.create_all(engine)