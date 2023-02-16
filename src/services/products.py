from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.products import Products
from src.models.schemas.products.products_request import ProductsRequest
from src.services.utils.modified_by_now import modified_by_now


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
    
    def add(self, products_schema: ProductsRequest, current_user_id: int) -> None:
        is_exist = (
            self.session
            .query(Products)
            .filter(Products.name == products_schema.name)
            .count()
        )
        if is_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        product = Products(
            name=products_schema.name,
            created_by=current_user_id,
            modified_by=current_user_id,
        )
        self.session.add(product)
        self.session.commit()

    def update(self, product_id: int, products_schema: ProductsRequest, current_user: dict) -> Products:
        product = self.get(product_id)
        for field, value in products_schema:
            setattr(product, field, value)
        modified_by_now(product, current_user)
        self.session.commit()
        return product

    def delete(self, product_id: int) -> None:
        product = self.get(product_id)
        self.session.delete(product)
        self.session.commit()
