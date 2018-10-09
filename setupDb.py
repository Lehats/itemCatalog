#!/usr/bin/env python3

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
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




engine = create_engine('sqlite:///parts.db')

Base.metadata.create_all(engine)