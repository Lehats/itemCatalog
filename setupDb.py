#!/usr/bin/env python3

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Parts(Base):
    __tablename__ = 'parts'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'description': self.description,
            'name': self.name,
        }


class Users(Base):
    __tablename__ = 'users'

    username = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    password_hash = Column(String(64))
    user = relationship(Parts, cascade="all, delete-orphan")

    def hashThePassword(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'username': self.name,
            'id': self.id,
        }


class Categories(Base):
    __tablename__ = 'categories'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    category = relationship(Parts, cascade="all, delete-orphan")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category': self.name,
            'id': self.id,
        }

engine = create_engine('sqlite:///parts.db')

Base.metadata.create_all(engine)
