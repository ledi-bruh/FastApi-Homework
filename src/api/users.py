from fastapi import APIRouter, Depends, HTTPException, status
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
def register(users_schema: UsersRequest, users_service: UsersService = Depends(), current_user: dict = Depends(get_current_user_info)) -> None:
    return users_service.register(users_schema, current_user.get('id'))


@router.post('/authorize', response_model=JwtToken, name='Авторизация пользователя')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), users_service: UsersService = Depends()) -> JwtToken:
    result = users_service.authorize(auth_schema.username, auth_schema.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ошибка авторизации')
    return result


@router.get('/get/{user_id}', response_model=UsersResponse, name='Получить пользователя', dependencies=[Depends(allow_work_with_users)])
def get(user_id: int, users_service: UsersService = Depends()):
    return get_with_check(user_id, users_service)


def get_with_check(user_id: int, users_service: UsersService):
    result = users_service.get(user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
    return result


@router.get('/all', response_model=List[UsersResponse], name='Получить всех пользователей', dependencies=[Depends(allow_work_with_users)])
def all(users_service: UsersService = Depends()):
    # ! убрать ошибку, типа пусто тоже норм?
    result = users_service.all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователи отсутствуют')
    return result


@router.put('/update/{user_id}', response_model=UsersResponse, name='Изменить пользователя', dependencies=[Depends(allow_work_with_users)])
def update(user_id: int, users_schema: UsersRequest, users_service: UsersService = Depends()):
    get_with_check(user_id, users_service)
    return users_service.update(user_id, users_schema)


@router.delete('/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить пользователя', dependencies=[Depends(allow_work_with_users)])
def delete(user_id: int, users_service: UsersService = Depends()):
    get_with_check(user_id, users_service)
    return users_service.delete(user_id)
