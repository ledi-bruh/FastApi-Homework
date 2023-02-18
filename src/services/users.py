from datetime import datetime, timezone, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.orm import Session
from src.core.settings import settings
from src.db.db import get_session
from src.models.users import Users
from src.models.schemas.users.users_request import UsersRequest
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.utils.modify_by_now import modify_by_now
from src.services.utils.create_by import create_by


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/users/authorize')


def get_current_user_info(token: str = Depends(oauth2_schema)) -> dict:
    return UsersService.verify_token(token)


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password_text: str, password_hash: str) -> bool:
        return pbkdf2_sha256.verify(password_text, password_hash)

    @staticmethod
    def create_token(user_id: int, user_role: str) -> JwtToken:
        now = datetime.now(timezone.utc)
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'sub': str(user_id),  # ! обязательно str?
            'role': user_role,
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        
        return JwtToken(access_token=token)

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный токен')

        user_info_from_token = {
            'id': payload.get('sub'),
            'role': payload.get('role'),
        }
        
        return user_info_from_token

    def register(self, users_schema: UsersRequest, current_user_id: int) -> None:
        is_exist = (
            self.session
            .query(Users)
            .filter(Users.username == users_schema.username)
            .count()
        )
        if is_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        user = create_by(Users(), users_schema, current_user_id)
        setattr(user, 'password_hashed', self.hash_password(users_schema.password_text))  # ! change_password
        
        self.session.add(user)
        self.session.commit()

    def authorize(self, username: str, password_text: str) -> Optional[JwtToken]:
        user = (
            self.session
            .query(Users)
            .filter(Users.username == username)
            .first()
        )

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not self.verify_password(password_text, user.password_hashed):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return self.create_token(user.id, user.role)

    def all(self) -> List[Users]:
        users = (
            self.session
            .query(Users)
            .order_by(Users.id.asc())
            .all()
        )
        return users

    def get(self, user_id: int) -> Users:
        user = (
            self.session
            .query(Users)
            .filter(Users.id == user_id)
            .one_or_none()
        )
        return user
    
    def get_with_check(self, user_id: int):
        result = self.get(user_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        return result

    def update(self, user_id: int, users_schema: UsersRequest, current_user: dict) -> Users:
        user = self.get_with_check(user_id)
        user_with_same_name = (
            self.session
            .query(Users)
            .filter(Users.username == users_schema.username)
            .first()
        )
        if user_with_same_name and user_with_same_name.id != user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
            
        modify_by_now(user, users_schema, current_user)
        setattr(user, 'password_hashed', self.hash_password(users_schema.password_text))
        
        self.session.commit()
        return user

    def delete(self, user_id: int):
        user = self.get_with_check(user_id)
        self.session.delete(user)
        self.session.commit()
