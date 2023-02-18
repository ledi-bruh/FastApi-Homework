from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.models.schemas.tanks.tanks_request import TanksRequest
from src.models.schemas.tanks.tanks_response import TanksResponse
from src.services.tanks import TanksService
from src.services.users import get_current_user_info


router = APIRouter(
    prefix='/tanks',
    tags=['tanks'],
    dependencies=[Depends(get_current_user_info)],
)


@router.get('/get/{tank_id}', response_model=TanksResponse, name='Получить данные о резервуаре')
def get(tank_id: int, tanks_service: TanksService = Depends()):
    return tanks_service.get_with_check(tank_id)


@router.get('/all', response_model=List[TanksResponse], name='Получить данные о всех резервуарах')
def all(tanks_service: TanksService = Depends()):
    return tanks_service.all()


@router.post('/add', status_code=status.HTTP_201_CREATED, name='Добавить резервуар')
def add(tanks_schema: TanksRequest, tanks_service: TanksService = Depends(), current_user: dict = Depends(get_current_user_info)):
    return tanks_service.add(tanks_schema, current_user.get('id'))


@router.put('/update/{tank_id}', response_model=TanksResponse, name='Изменить данные о резервуаре')
def update(tank_id: int, tanks_schema: TanksRequest, tanks_service: TanksService = Depends(), current_user: dict = Depends(get_current_user_info)):
    return tanks_service.update(tank_id, tanks_schema, current_user)


@router.delete('/delete/{tank_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить данные о резервуаре')
def delete(tank_id: int, tanks_service: TanksService = Depends()):
    return tanks_service.delete(tank_id)
