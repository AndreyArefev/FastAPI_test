import datetime

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import model_db
from app.db.database import get_session
from app.schemas import accounts

class UserService:
    @staticmethod
    def deposit(account_balance, amount) -> float:
        account_balance += amount
        return account_balance

    @staticmethod
    def withdrow(account_balance, amount) -> float:
        if account_balance - amount >= 0:
            account_balance -= amount
        else:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Недостаточно средств',
                                headers={'WWW-Authenticate': 'Bearer'},
                                )
        return account_balance
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all_products (self) -> List[model_db.Product]:
        products = (
            self.session
            .query(model_db.Product)
            .order_by(
                model_db.Product.product_name.desc(),
            )
            .all()
        )
        print(products)
        return products

    def create_account (self,
                        user_id: int,
                        account_data: accounts.AccountCreate,
                        ) -> model_db.Account:
        if not self.check_name_account(account_data.account_name, user_id):
            account = model_db.Account(
                user_id=user_id,
                account_name = account_data.account_name,
                account_balance=0)
            self.session.add(account)
            self.session.commit()
            return account
        else:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Аккаунт с данным именем уже существует. Выберите другое имя аккаунта',
                                headers={'WWW-Authenticate': 'Bearer'},
                                )

    def buy_product(self,
                     user_id: int,
                     account_name: str,
                     product_id: int):
        current_account = self.check_name_account(account_name, user_id)
        if current_account:
            product_price = self.check_product(product_id)
            return self.make_transaction(current_account, type_operation='Withdrow', amount=product_price)
        else:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Аккаунта с данным именем не существует. Выберите другой аккаунт',
                                headers={'WWW-Authenticate': 'Bearer'},
                                )

    def get_accounts(self,
                    user_id: int) -> List[model_db.Account]:
        all_accounts_user = (
            self.session
            .query(model_db.Account)
            .filter(model_db.Account.user_id == user_id)
            .all()
        )
        return all_accounts_user

    def account_payment(self,
                       user_id: int,
                       account: accounts.AccountPayment) -> model_db.Transaction:
        current_account = self.check_name_account(account.account_name, user_id)
        if current_account:
            new_account_balance = self.deposit(current_account.account_balance,
                                               account.amount_payment,
                                               )
            transaction = model_db.Transaction(
                user_id = user_id,
                account_id = current_account.account_id,
                type_operation = 'Deposit',
                amount = account.amount_payment,
                date_transaction=datetime.date.today())
            self.session.add(transaction)
            self.session.query(model_db.Account) \
                .filter(model_db.Account.account_id == current_account.account_id) \
                .update({'account_balance': new_account_balance})
            self.session.commit()
            return transaction
        else:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Аккаунта с данным именем не существует. Выберите другой аккаунт',
                                headers={'WWW-Authenticate': 'Bearer'},
                                )

    def make_transaction(self,
                         current_account: model_db.Account,
                         type_operation: str,
                         amount: float,
                         ) -> model_db.Transaction:
        if type_operation == 'Withdrow':
            new_account_balance = self.withdrow(current_account.account_balance,
                                                amount)
        elif type_operation == 'Deposit':
            new_account_balance = self.deposit(current_account.account_balance,
                                               amount)
        else:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Недопустимая операция')
        transaction = model_db.Transaction(
            user_id=current_account.user_id,
            account_id=current_account.account_id,
            type_operation=type_operation,
            amount=amount,
            date_transaction=datetime.date.today())
        self.session.add(transaction)
        self.session.query(model_db.Account) \
            .filter(model_db.Account.account_id == current_account.account_id) \
            .update({'account_balance': new_account_balance})
        self.session.commit()
        return transaction

    def check_name_account(self,
                           account_name: str,
                           user_id: int,
                           ) -> Optional[model_db.Account]:
        checking_name_account = (
            self.session
            .query(model_db.Account)
            .filter(
                model_db.Account.user_id == user_id,
                model_db.Account.account_name == account_name,
            )
            .first()
        )
        return checking_name_account


    def check_product(self,
                            product_id: int,
                            ) -> float:
        checking_product = (
            self.session
            .query(model_db.Product)
            .filter(
                model_db.Product.product_id == product_id,
            )
            .first()
        )
        if checking_product:
            return checking_product.product_price
        else:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Данного продукта нет в наличии. Выберите другой продукт')





