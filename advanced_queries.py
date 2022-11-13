from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import time_it
import models
import schemas


# @time_it.time_it_once
def get_total_sold_quantity_by_product(product_id: int, db: Session):
    return db.query(func.sum(models.Sale.quantity)).where(models.Sale.product_id == product_id).scalar()


def get_total_sold_price_by_product(product_id: int, db: Session):
    return db.query(func.sum(models.Sale.price)).where(models.Sale.product_id == product_id).scalar()


def get_total_sold_price_by_product_over_period(start_date: datetime, end_date: datetime, product_id: int, db: Session):
    pass