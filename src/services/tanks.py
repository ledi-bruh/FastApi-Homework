from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.tanks import Tanks
from src.models.schemas.tanks.tanks_request import TanksRequest
from src.services.users import modify_by, create_by
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

        if not tank:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Резервуар не найден')

        return tank
    
    def add(self, tanks_schema: TanksRequest, current_user: dict) -> None:
        ProductsService(self.session).get(tanks_schema.product_id)
        
        tank = create_by(Tanks(), tanks_schema, current_user)

        self.session.add(tank)
        self.session.commit()

    def update(self, tank_id: int, tanks_schema: TanksRequest, current_user: dict) -> Tanks:
        tank = self.get(tank_id)
        ProductsService(self.session).get(tanks_schema.product_id)

        for field, value in tanks_schema:
            setattr(tank, field, value)
        modify_by(tank, current_user)

        self.session.commit()
        return tank

    def delete(self, tank_id: int) -> None:
        tank = self.get(tank_id)
        self.session.delete(tank)
        self.session.commit()
    
    def set_capacity(self, tank_id: int, current_capacity: float, current_user: dict):
        tank = self.get(tank_id)
        
        setattr(tank, 'current_capacity', current_capacity)
        modify_by(tank, current_user)
        
        self.session.commit()
        return tank
