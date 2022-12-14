from pydantic import BaseModel
from datetime import datetime, date


# Shop


class Shop(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ShopCreate(BaseModel):
    name: str


# Product


class Product(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    price: float


# Receipt


class Receipt(BaseModel):
    id: int
    date: datetime
    total_price: float
    shop_id: int

    class Config:
        orm_mode = True


class ReceiptCreate(BaseModel):
    date: datetime
    total_price: float
    shop_id: int


# Sale


class Sale(BaseModel):
    id: int
    quantity: int
    price: float
    receipt_id: int
    product_id: int

    class Config:
        orm_mode = True


class SaleCreate(BaseModel):
    quantity: int
    price: float
    receipt_id: int
    product_id: int


# Advanced Queries Schemas

class Period(BaseModel):
    start_date: datetime
    end_date: datetime


class ProductPeriod(BaseModel):
    start_date: datetime
    end_date: datetime
    product_id: int


class ProductShopPeriod(BaseModel):
    product_id: int
    shop_id: int
    start_date: datetime
    end_date: datetime
