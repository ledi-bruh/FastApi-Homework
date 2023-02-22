from fastapi import APIRouter, Depends, status
from typing import List
from src.models.schemas.products.products_request import ProductsRequest
from src.models.schemas.products.products_response import ProductsResponse
from src.services.products import ProductsService
from src.services.users import get_current_user_info


router = APIRouter(
    prefix='/products',
    tags=['products'],
    dependencies=[Depends(get_current_user_info)],
)


@router.get('/get/{product_id}', response_model=ProductsResponse, name='Получить продукт')
def get(product_id: int, products_service: ProductsService = Depends()):
    return products_service.get_with_check(product_id)


@router.get('/all', response_model=List[ProductsResponse], name='Получить все продукты')
def all(products_service: ProductsService = Depends()):
    return products_service.all()


@router.post('/add', status_code=status.HTTP_201_CREATED, name='Добавление продукта')
def add(products_schema: ProductsRequest, products_service: ProductsService = Depends(), current_user: dict = Depends(get_current_user_info)):
    return products_service.add(products_schema, current_user)


@router.put('/update/{product_id}', response_model=ProductsResponse, name='Изменить продукт')
def update(product_id: int, products_schema: ProductsRequest, products_service: ProductsService = Depends(), current_user: dict = Depends(get_current_user_info)):
    return products_service.update(product_id, products_schema, current_user)


@router.delete('/delete/{product_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить продукт')
def delete(product_id: int, products_service: ProductsService = Depends()):
    return products_service.delete(product_id)
