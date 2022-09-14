from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
)

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from typing import List
from app.schemas import products, accounts, transactions, users
from app.crud.auth import get_current_user
from app.crud.user import UserService

router = APIRouter(
    prefix='/user',
    tags=['user'],
)

@router.get(
    '/',
    response_model=List[products.Product],
)
def get_products(
    user_service: UserService = Depends(),
    user: users.User = Depends(get_current_user),
):
    return user_service.all_products()

@router.post(
    '/',
    response_model=accounts.AccountBase,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    account_data: accounts.AccountCreate,
    user: users.User = Depends(get_current_user),
    user_service: UserService = Depends(),
):
    return user_service.create_account(user.user_id, account_data)

@router.put(
    '/',
    response_model=transactions.Transaction,
)
def buy_product(
    current_purchase: accounts.BuyProduct,
    user: users.User = Depends(get_current_user),
    user_service: UserService = Depends(),
):
    return user_service.buy_product(user.user_id, current_purchase.account_name, current_purchase.product_id)

@router.get(
    '/accounts',
    response_model=List[accounts.AccountTransactions]
)
def get_accounts(
        user: users.User = Depends(get_current_user),
        user_service: UserService = Depends(),
):
    return user_service.get_accounts(user.user_id)

@router.post(
    '/payment/webhook',
    response_model=transactions.Transaction,
    status_code=status.HTTP_201_CREATED,
)
def account_payment(
    current_account: accounts.AccountPayment,
    user: users.User = Depends(get_current_user),
    user_service: UserService = Depends(),
):
    return user_service.account_payment(user.user_id, current_account)

#5. Просмотр баланса всех счетов и историю транзакций
#6. Зачисление средств на счёт, выполняется с помощью эндпоинта [POST] /payment/webhook симулирует начисление со стороннего сервиса.


