from io import StringIO
from typing import List
from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.operations import Operations
from src.models.schemas.operations.operations_request import OperationsRequest
from src.services.utils.modify_by_now import modify_by_now
from src.services.utils.create_by import create_by
from src.services.tanks import TanksService
from src.services.products import ProductsService
from src.services.files import download


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Operations]:
        operations = (
            self.session
            .query(Operations)
            .order_by(Operations.id.asc())
            .all()
        )
        return operations

    def get(self, operation_id: int) -> Operations:
        operation = (
            self.session
            .query(Operations)
            .filter(Operations.id == operation_id)
            .one_or_none()
        )
        return operation

    def get_with_check(self, operation_id: int) -> Operations:
        result = self.get(operation_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Операция не найдена')
        return result
    
    def add(self, operations_schema: OperationsRequest, current_user: dict) -> None:
        # ! Как следовало бы правильно вызвать эту проверку?
        TanksService(self.session).get_with_check(operations_schema.tank_id)
        ProductsService(self.session).get_with_check(operations_schema.product_id)
        
        operation = create_by(Operations(), operations_schema, current_user)
        
        self.session.add(operation)
        self.session.commit()

    def update(self, operation_id: int, operations_schema: OperationsRequest, current_user: dict) -> Operations:
        operation = self.get_with_check(operation_id)
        TanksService(self.session).get_with_check(operations_schema.tank_id)
        ProductsService(self.session).get_with_check(operations_schema.product_id)
        
        for field, value in operations_schema:
            setattr(operation, field, value)
        modify_by_now(operation, current_user)
        
        self.session.commit()
        return operation

    def delete(self, operation_id: int) -> None:
        operation = self.get_with_check(operation_id)
        self.session.delete(operation)
        self.session.commit()
    
    def all_by_tank_id(self, tank_id: int) -> List[Operations]:
        operations = (
            self.session
            .query(Operations)
            .filter(Operations.tank_id == tank_id)
            .order_by(Operations.id.asc())
            .all()
        )
        return operations

    def get_report(self, tank_id: int, product_id: int, date_start: datetime, date_end: datetime) -> StringIO:
        operations = (
            self.session
            .query(Operations)
            .filter(Operations.tank_id == tank_id, Operations.product_id == product_id)
            # ! диапазон из параметров внутри диапазона операции
            .filter(Operations.date_start <= date_start, Operations.date_end >= date_end)
            .order_by(Operations.id.asc())
            .all()
        )
        
        if not operations:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Операций по данным параметрам не найдено')
        
        # ! как лучше получить только эти поля?
        fieldnames = ['id', 'mass', 'date_start', 'date_end', 'tank_id', 'product_id', 'created_at', 'created_by', 'modified_at', 'modified_by']
        report = download(operations, fieldnames)
        
        return report
