from pydantic import BaseModel

class ProductBase(BaseModel):
    product_name: str

    class Config:
        orm_mode = True


class ProductInformation(ProductBase):
    product_description: str
    product_price: float


class ProductCreate(ProductInformation):
    pass


class ProductUpdate(ProductInformation):
    pass


class Product(ProductCreate, ProductUpdate):
    product_id: int

