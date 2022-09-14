from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Float,
    Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
#создание базового класса для всех таблиц и классов связанных с ними

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(String)



class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    product_description = Column(Text)
    product_price = Column(Float)


class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True)
    account_name = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    account_balance = Column(Float)
    user = relationship("User", backref="accounts")


class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), index=True)
    type_operation = Column(String)
    amount = Column(Float)
    user = relationship("User", backref="transactions")
    account = relationship("Account", backref="transactions")