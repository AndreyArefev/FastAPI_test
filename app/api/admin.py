from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
    Response,
)

from app.schemas import users, products
from app.crud.auth import RoleChecker
from app.crud.admin import AdminService
from typing import List

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)
allow_access_resource = RoleChecker(['admin'])


@router.get(
    '/products',
    response_model=List[products.ProductInformation],
    dependencies=[Depends(allow_access_resource)],
)
def get_products(
    admin_service: AdminService = Depends(),
):
    return admin_service.get_all_products()


@router.post(
    '/products',
    response_model=products.Product,
    dependencies=[Depends(allow_access_resource)],
    status_code=status.HTTP_201_CREATED,
)
def create_products(
    product_data: products.ProductCreate,
    admin_service: AdminService = Depends(),
):
    return admin_service.create_product(product_data)

@router.get(
    '/products/{product_id}',
    response_model=products.Product,
    dependencies=[Depends(allow_access_resource)],
)
def get_product(
    product_id: int,
    admin_service: AdminService = Depends(),
):
    return admin_service.get_product(product_id)


@router.put(
    '/products/{product_id}',
    response_model=products.Product,
    dependencies=[Depends(allow_access_resource)],
)
def update_product(
    product_id: int,
    product_data: products.ProductUpdate,
    admin_service: AdminService = Depends(),
):
    return admin_service.update_product(product_id, product_data)

@router.delete(
    '/products/{product_id}',
    dependencies=[Depends(allow_access_resource)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    admin_service: AdminService = Depends(),
):
    admin_service.delete_product(product_id)
    return Response (status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/users',
    response_model = List[users.UserAccounts],
    dependencies=[Depends(allow_access_resource)],
)
def get_all_users(
    admin_service: AdminService = Depends(),
):
    return admin_service.get_all_users()


@router.get(
    '/users/{user_id}',
    response_model = users.UserAccounts,
    dependencies=[Depends(allow_access_resource)],
)
def get_users(
    user_id: int,
    admin_service: AdminService = Depends(),
):
    return admin_service.get_user(user_id)


@router.put(
    '/users/{user_id}',
    response_model = users.UserAccounts,
)
def status_users(
        user_id: int,
        status_user: users.UserStatus,
        admin_service: AdminService = Depends(),
):
    return admin_service.status_user(user_id, status_user.is_active)

