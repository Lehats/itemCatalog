#!/usr/bin/env python3

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Parts(Base): 
    __tablename__ = 'parts' 

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(1000))
    category = Column(String(80))



engine = create_engine('sqlite:///parts.db')

Base.metadata.create_all(engine)