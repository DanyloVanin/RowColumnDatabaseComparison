from datetime import datetime

from sqlalchemy.sql import text
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import time_it
import models
import schemas


# @time_it.time_it_once
# Порахувати кількість проданого товару
def get_total_sold_quantity_by_product(db: Session):
    return db.query(func.sum(models.Sale.quantity)).scalar()


# Порахувати вартість проданого товару
def get_total_sold_price_by_product(db: Session):
    return db.query(func.sum(models.Sale.price)).scalar()


# Порахувати вартість проданого товару за період
def get_total_sold_price_by_product_over_period(start_date: datetime, end_date: datetime, db: Session):
    receipt_subquery = db.query(models.Receipt.id).filter(
        and_(models.Receipt.date >= start_date, models.Receipt.date <= end_date)).subquery()
    return db.query(func.sum(models.Sale.price)).filter(models.Sale.receipt_id.in_(receipt_subquery)).scalar()


# Порахувати скільки було придбано товару А в мазазині В за період С
def get_product_quantity_in_shop_over_period(start_date: datetime, end_date: datetime, product_id: int, shop_id: int,
                                             db: Session):
    receipt_subquery = db.query(models.Receipt.id).filter(
        and_(models.Receipt.date >= start_date, models.Receipt.date <= end_date),
        models.Receipt.shop_id == shop_id).subquery()
    return db.query(func.sum(models.Sale.price)).filter(
        and_(models.Sale.product_id == product_id, models.Sale.receipt_id.in_(receipt_subquery))).scalar()


# Порахувати скільки було придбано товару А в усіх магазинах за період С
def get_product_quantity_in_all_shops_over_period(start_date: datetime, end_date: datetime, product_id: int,
                                                  db: Session):
    receipt_subquery = db.query(models.Receipt.id).filter(
        and_(models.Receipt.date >= start_date, models.Receipt.date <= end_date)).subquery()
    return db.query(func.sum(models.Sale.price)).filter(
        and_(models.Sale.product_id == product_id, models.Sale.receipt_id.in_(receipt_subquery))).scalar()


# Порахувати сумарну виручку магазинів за період С
def get_total_revenue_over_period(start_date: datetime, end_date: datetime, db: Session):
    receipt_subquery = db.query(models.Receipt.id).filter(
        and_(models.Receipt.date >= start_date, models.Receipt.date <= end_date)).subquery()
    return db.query(func.sum(models.Sale.price)).filter(models.Sale.receipt_id.in_(receipt_subquery)).scalar()


# Вивести топ 10 купівель товарів по два за період С (наприклад масло, хліб - 1000 разів)
def get_top10_2product_combinations_over_period(start_date: datetime, end_date: datetime, db: Session):
    statement = text(f"""
    select s.product_id as product_1, 
       s2.product_id as product_2, 
       s3.product_id as product_3,
       s4.product_id as product_4,
       count(*) as number_of_sales, 
       string_agg(s.receipt_id::varchar, ',') as receipts 
        from sales s join sales s2 on s.product_id < s2.product_id join sales s3 on s2.product_id < s3.product_id join sales s4 on s3.product_id < s4.product_id 
        where s.receipt_id = s2.receipt_id and s2.receipt_id = s3.receipt_id and s3.receipt_id = s4.receipt_id 
            and s.receipt_id in (select id from receipts r where r."date">{start_date.isoformat()} and r."date"<{end_date.isoformat()})
        group by s.product_id ,s2.product_id , s3.product_id , s4.product_id 
        order by number_of_sales desc
        fetch first 10 rows only;""")

    result_set = db.execute(statement)
    result = []
    for row in result_set:
        print(row)
        result.append(row)
    return result