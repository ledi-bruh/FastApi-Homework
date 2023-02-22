from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from src.models.schemas.users.users_request import UsersRequest
from src.models.schemas.users.users_response import UsersResponse
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.users import UsersService
from src.services.users import get_current_user_info
from src.api.utils.role_checker import RoleChecker


router = APIRouter(
    prefix='/users',
    tags=['users'],
)

allow_work_with_users = RoleChecker(['admin'])


@router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация пользователя', dependencies=[Depends(allow_work_with_users)])
def register(users_schema: UsersRequest, users_service: UsersService = Depends(), current_user: dict = Depends(get_current_user_info)):
    """
    Регистрация пользователей доступна только администраторам.
    """
    return users_service.register(users_schema, current_user)


@router.post('/authorize', response_model=JwtToken, name='Авторизация пользователя')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), users_service: UsersService = Depends()) -> JwtToken:
    return users_service.authorize(auth_schema.username, auth_schema.password)


@router.get('/get/{user_id}', response_model=UsersResponse, name='Получить пользователя', dependencies=[Depends(allow_work_with_users)])
def get(user_id: int, users_service: UsersService = Depends()):
    """
    Доступно только администраторам.
    """
    return users_service.get(user_id)


@router.get('/all', response_model=List[UsersResponse], name='Получить всех пользователей', dependencies=[Depends(allow_work_with_users)])
def all(users_service: UsersService = Depends()):
    """
    Доступно только администраторам.
    """
    return users_service.all()


@router.put('/update/{user_id}', response_model=UsersResponse, name='Изменить пользователя', dependencies=[Depends(allow_work_with_users)])
def update(user_id: int, users_schema: UsersRequest, users_service: UsersService = Depends(), current_user: dict = Depends(get_current_user_info)):
    """
    Доступно только администраторам.
    """
    return users_service.update(user_id, users_schema, current_user)


@router.delete('/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить пользователя', dependencies=[Depends(allow_work_with_users)])
def delete(user_id: int, users_service: UsersService = Depends()):
    """
    Доступно только администраторам.
    """
    return users_service.delete(user_id)
