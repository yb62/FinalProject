from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    full_name = Column(String)


class Token(Base):
    __tablename__ = "tokens"
    token = Column(String, primary_key=True)
    user_id = Column(Integer)


class UserIn(BaseModel):
    username: str
    password: str
    full_name: str


class UserOut(BaseModel):
    username: str
    fullName: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str


def create_tables(engine):
    Base.metadata.create_all(bind=engine)

def convert_user(user: User) -> UserOut:
    return UserOut(username=user.username, fullName=user.full_name)

def convert_users(users: List[User]) -> List[UserOut]:
    return [convert_user(u) for u in users]