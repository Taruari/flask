from sqlalchemy import Column, String, Integer, Identity
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Base, Movie - class


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Identity(always=False), primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(500))
   

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
           
        }
