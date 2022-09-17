from datetime import date
from pydantic import BaseModel

class TransactionBase(BaseModel):
    user_id: int
    account_id: int

class TransactionMake(TransactionBase):
    type_operation: str
    amount: float

    class Config:
        orm_mode = True


class Transaction(TransactionMake):
    transaction_id: int
    date_transaction: date

