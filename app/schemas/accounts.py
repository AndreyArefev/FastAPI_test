from pydantic import BaseModel
from typing import List, Optional
from .transactions import Transaction


class AccountCreate(BaseModel):
    account_name: str

    class Config:
        orm_mode = True

class BuyProduct(AccountCreate):
    product_id: int

class AccountPayment(AccountCreate):
    amount_payment: float


class AccountBase(AccountCreate):
    account_id: int
    account_balance: float = 0


class Account(AccountBase):
    user_id: int


class AccountTransactions(AccountBase):
    transactions: List[Transaction]


