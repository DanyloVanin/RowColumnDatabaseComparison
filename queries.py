from sqlalchemy.orm import Session

import models
import schemas


# Shop


def create_shop(db: Session, shop: schemas.ShopCreate):
    entity = models.Shop(name=shop.name)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_shop_by_name(db: Session, name: str):
    return db.query(models.Shop).filter(models.Shop.name == name).first()


def get_shop_by_id(db: Session, shop_id: int):
    return db.query(models.Shop).filter(models.Shop.id == shop_id).first()


def get_shops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Shop).offset(skip).limit(limit).all()


# Product


def create_product(db: Session, product: schemas.ProductCreate):
    entity = models.Product(name=product.name, price=product.price)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


# Receipt


def create_receipt(db: Session, receipt: schemas.ReceiptCreate):
    entity = models.Receipt(shop_id=receipt.shop_id, total_price=receipt.total_price, date=receipt.date)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_receipt_by_id(db: Session, receipt_id: int):
    return db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()


def get_receipts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Receipt).offset(skip).limit(limit).all()


# Sale


def create_sale(db: Session, sale: schemas.SaleCreate):
    entity = models.Sale(receipt_id=sale.receipt_id, quantity=sale.quantity,
                         price=sale.price, product_id=sale.product_id)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_sale_by_id(db: Session, sale_id: int):
    return db.query(models.Sale).filter(models.Sale.id == sale_id).first()


def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()

