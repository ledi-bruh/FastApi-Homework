from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.products import Products
from src.models.schemas.products.products_request import ProductsRequest
from src.services.utils.modify_by_now import modify_by_now
from src.services.utils.create_by import create_by


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Products]:
        products = (
            self.session
            .query(Products)
            .order_by(Products.id.asc())
            .all()
        )
        return products

    def get(self, product_id: int) -> Products:
        product = (
            self.session
            .query(Products)
            .filter(Products.id == product_id)
            .one_or_none()
        )
        return product
    
    def get_with_check(self, product_id: int) -> Products:
        result = self.get(product_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Продукт не найден')
        return result
    
    def add(self, products_schema: ProductsRequest, current_user_id: int) -> None:
        product = create_by(Products(), products_schema, current_user_id)
        self.session.add(product)
        self.session.commit()

    def update(self, product_id: int, products_schema: ProductsRequest, current_user: dict) -> Products:
        product = self.get_with_check(product_id)
        modify_by_now(product, products_schema, current_user)
        self.session.commit()
        return product

    def delete(self, product_id: int) -> None:
        product = self.get_with_check(product_id)
        self.session.delete(product)
        self.session.commit()
