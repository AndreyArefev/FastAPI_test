from fastapi import (
    Depends,
    HTTPException,
    status,
)

from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import model_db
from app.db.database import get_session
from app.schemas import products, users


class AdminService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all_products(self) -> List[products.Product]:
        get_all_products = (
            self.session
            .query(model_db.Product)
            .order_by(model_db.Product.product_id)
            .all()
        )
        self.session.commit()
        return get_all_products

    def create_product(self, product_data: products.ProductCreate) -> products.ProductCreate:
        create_product = model_db.Product(
            product_name=product_data.product_name,
            product_description=product_data.product_description,
            product_price=product_data.product_price,
        )
        self.session.add(create_product)
        self.session.commit()
        return create_product

    def get_product(self,
                    product_id) -> products.Product:
        return self._get_product(product_id)

    def update_product(self,
                       product_id,
                       product_data) -> products.ProductUpdate:
        update_product = self._get_product(product_id)
        for field, value in product_data:
            setattr(update_product, field, value)
        self.session.commit()
        return update_product

    def delete_product(self,
                       user_id):
        product = self._get_user(user_id)
        self.session.delete(product)
        self.session.commit()

    def _get_product(self,
                     product_id) -> products.Product:
        _get_product = (
            self.session
            .query(model_db.Product)
            .filter(model_db.Product.product_id == product_id)
            .first()
        )
        if not _get_product:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _get_product

    def get_all_users(self) -> List[users.UserAccounts]:
        all_users = (
            self.session
            .query(model_db.User)
            .all()
            )
        return all_users

    def get_user(self,
                 user_id) -> users.UserAccounts:
        return self._get_user(user_id)

    def status_user(self,
                    user_id,
                    is_active) -> users.UserAccounts:
        status_user = self._get_user(user_id)
        status_user.is_active = is_active
        self.session.commit()
        return status_user

    def _get_user(self,
                  user_id) -> users.UserAccounts:
        _get_user = (
            self.session
            .query(model_db.User)
            .filter(model_db.User.user_id == user_id)
            .first()
        )
        if not _get_user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _get_user