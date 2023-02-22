from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from typing import List
from datetime import datetime
from src.models.schemas.operations.operations_request import OperationsRequest
from src.models.schemas.operations.operations_response import OperationsResponse
from src.services.operations import OperationsService
from src.services.users import get_current_user_info


router = APIRouter(
    prefix='/operations',
    tags=['operations'],
    dependencies=[Depends(get_current_user_info)],
)


@router.get('/get/{operation_id}', response_model=OperationsResponse, name='Получить данные об операции')
def get(operation_id: int, operations_service: OperationsService = Depends()):
    return operations_service.get(operation_id)


@router.get('/all', response_model=List[OperationsResponse], name='Получить данные о всех операциях')
def all(operations_service: OperationsService = Depends()):
    return operations_service.all()


@router.post('/add', status_code=status.HTTP_201_CREATED, name='Добавить операцию')
def add(operations_schema: OperationsRequest, operations_service: OperationsService = Depends(), current_user: dict = Depends(get_current_user_info)):
    return operations_service.add(operations_schema, current_user)


@router.put('/update/{operation_id}', response_model=OperationsResponse, name='Изменить данные об операции')
def update(operation_id: int, operations_schema: OperationsRequest, operations_service: OperationsService = Depends(), current_user: dict = Depends(get_current_user_info)):
    return operations_service.update(operation_id, operations_schema, current_user)


@router.delete('/delete/{operation_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить данные об операции')
def delete(operation_id: int, operations_service: OperationsService = Depends()):
    return operations_service.delete(operation_id)


@router.get('/all/{tank_id}', response_model=List[OperationsResponse], name='Получить данные о всех операциях с резервуаром')
def all_by_tank_id(tank_id: int, operations_service: OperationsService = Depends()):
    return operations_service.all_by_tank_id(tank_id)

@router.get('/download/report/', name='Скачать отчет по операциям')
def download_report_csv(tank_id: int, product_id: int, date_start: datetime, date_end: datetime, operations_service: OperationsService = Depends()):
    report = operations_service.get_report(tank_id, product_id, date_start, date_end)
    return StreamingResponse(report, media_type='text/csv', headers={'Content-Disposition': 'attachment; filename=report_operations.csv'})
