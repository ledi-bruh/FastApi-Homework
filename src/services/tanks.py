from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.tanks import Tanks
from src.models.schemas.tanks.tanks_request import TanksRequest
from src.services.utils.modify_by_now import modify_by_now
from src.services.utils.create_by import create_by
from src.services.products import ProductsService


class TanksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Tanks]:
        tanks = (
            self.session
            .query(Tanks)
            .order_by(Tanks.id.asc())
            .all()
        )
        return tanks

    def get(self, tank_id: int) -> Tanks:
        tank = (
            self.session
            .query(Tanks)
            .filter(Tanks.id == tank_id)
            .one_or_none()
        )
        return tank

    def get_with_check(self, tank_id: int) -> Tanks:
        result = self.get(tank_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Резервуар не найден')
        return result
    
    def add(self, tanks_schema: TanksRequest, current_user_id: int) -> None:            
        ProductsService(self.session).get_with_check(tanks_schema.product_id)
        
        tank = create_by(Tanks(), tanks_schema, current_user_id)
        
        self.session.add(tank)
        self.session.commit()

    def update(self, tank_id: int, tanks_schema: TanksRequest, current_user: dict) -> Tanks:
        tank = self.get_with_check(tank_id)
        ProductsService(self.session).get_with_check(tanks_schema.product_id)
        
        modify_by_now(tank, tanks_schema, current_user)
        
        self.session.commit()
        return tank

    def delete(self, tank_id: int) -> None:
        tank = self.get_with_check(tank_id)
        self.session.delete(tank)
        self.session.commit()
