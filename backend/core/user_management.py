import os
from hashlib import sha256
from models.user_base import *

class UserManagement:
    
    @staticmethod
    def create_user(session, username: str, password: str, fullname: str):
        user = User(username=username, password=password, full_name=fullname)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def get_user(session, username: str):
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    def generate_token(username: str):
        return sha256(bytes(f"{username}{os.urandom(1024)}", encoding='utf-8')).hexdigest()

    @staticmethod
    def create_access_token(session, user):
        token = UserManagement.generate_token(user.username)
        session.add(Token(token=token, user_id=user.id))
        session.commit()
        return token

    @staticmethod
    def get_current_user(session, token: str):
        token_obj = session.query(Token).filter(Token.token == token).first()
        if not token_obj:
            return None
        return session.query(User).filter(User.id == token_obj.user_id).first()

    @staticmethod
    def authenticate_user(session, username: str, password: str):
        return session.query(User).filter(User.username == username, User.password == password).first()

    