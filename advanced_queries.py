from datetime import datetime

from sqlalchemy.sql import text
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import time_it
import models
import schemas


# Порахувати кількість проданого товару
@time_it.time_it_once(description="Порахувати кількість проданого товару")
def get_total_sold_quantity_by_product(db: Session):
    return db.query(func.sum(models.Sale.quantity)).scalar()


# Порахувати вартість проданого товару
@time_it.time_it_once(description="Порахувати вартість проданого товару")
def get_total_sold_price_by_product(db: Session):
    return db.query(func.sum(models.Sale.price)).scalar()


# Порахувати вартість проданого товару за період
@time_it.time_it_once(description="Порахувати вартість проданого товару за період")
def get_total_sold_price_by_product_over_period(start_date: datetime, end_date: datetime, db: Session):
    receipt_subquery = db.query(models.Receipt.id).filter(
        and_(models.Receipt.date >= start_date, models.Receipt.date <= end_date)).subquery()
    return db.query(func.sum(models.Sale.price)).filter(models.Sale.receipt_id.in_(receipt_subquery)).scalar()


# Порахувати скільки було придбано товару А в мазазині В за період С
@time_it.time_it_once(description="Порахувати вартість проданого товару за період")
def get_product_quantity_in_shop_over_period(start_date: datetime, end_date: datetime, product_id: int, shop_id: int,
                                             db: Session):
    receipt_subquery = db.query(models.Receipt.id).filter(
        and_(models.Receipt.date >= start_date, models.Receipt.date <= end_date),
        models.Receipt.shop_id == shop_id).subquery()
    return db.query(func.sum(models.Sale.price)).filter(
        and_(models.Sale.product_id == product_id, models.Sale.receipt_id.in_(receipt_subquery))).scalar()


# Порахувати скільки було придбано товару А в усіх магазинах за період С
@time_it.time_it_once(description="Порахувати вартість проданого товару за період")
def get_product_quantity_in_all_shops_over_period(start_date: datetime, end_date: datetime, product_id: int,
                                                  db: Session):
    receipt_subquery = db.query(models.Receipt.id).filter(
        and_(models.Receipt.date >= start_date, models.Receipt.date <= end_date)).subquery()
    return db.query(func.sum(models.Sale.price)).filter(
        and_(models.Sale.product_id == product_id, models.Sale.receipt_id.in_(receipt_subquery))).scalar()


# Порахувати сумарну виручку магазинів за період С
@time_it.time_it_once(description="Порахувати вартість проданого товару за період")
def get_total_revenue_over_period(start_date: datetime, end_date: datetime, db: Session):
    receipt_subquery = db.query(models.Receipt.id).filter(
        and_(models.Receipt.date >= start_date, models.Receipt.date <= end_date)).subquery()
    return db.query(func.sum(models.Sale.price)).filter(models.Sale.receipt_id.in_(receipt_subquery)).scalar()


# Вивести топ 10 купівель товарів по два за період С (наприклад масло, хліб - 1000 разів)
@time_it.time_it_once(description="Порахувати вартість проданого товару за період")
def get_top10_2product_combinations_over_period(start_date: datetime, end_date: datetime, db: Session, dbtype="row"):
    statement = text(f"""
    select s.product_id as product_1, 
       s2.product_id as product_2, 
       count(*) as number_of_sales, 
       string_agg(s.receipt_id::varchar, ',') as receipts 
        from sales s join sales s2 on s.product_id < s2.product_id
        where s.receipt_id = s2.receipt_id
            and s.receipt_id in (select id from receipts r where r."date">'{start_date.isoformat(sep=" ")}' and r."date"<'{end_date.isoformat(sep=" ")}')
        group by s.product_id ,s2.product_id
        order by number_of_sales desc
        fetch first 10 rows only;""")
    if 'column' in dbtype:
        statement = text(f"""
            select s.product_id as product_1, 
               s2.product_id as product_2, 
               count(*) as number_of_sales, 
               LISTAGG(s.receipt_id, ',') as receipts
                from sales s join sales s2 on s.product_id < s2.product_id
                where s.receipt_id = s2.receipt_id
                    and s.receipt_id in (select id from receipts r where r."date">TO_DATE('{start_date.date().isoformat()}','YYYY-MM-DD') and r."date"<TO_DATE('{end_date.date().isoformat()}','YYYY-MM-DD') )
                group by s.product_id ,s2.product_id
                order by number_of_sales desc
                fetch first 10 rows only""")
    result_set = db.execute(statement)
    result = []
    for row in result_set:
        print(row)
        result.append(row)
    return result


# Вивести топ 10 купівель товарів по три за період С (наприклад молоко, масло, хліб - 1000 разів)
@time_it.time_it_once(description="Порахувати вартість проданого товару за період")
def get_top10_3product_combinations_over_period(start_date: datetime, end_date: datetime, db: Session, dbtype="row"):
    statement = text(f"""
    select s.product_id as product_1, 
       s2.product_id as product_2, 
       s3.product_id as product_3,
       count(*) as number_of_sales, 
       string_agg(s.receipt_id::varchar, ',') as receipts 
    from sales s join sales s2 on s.product_id < s2.product_id join sales s3 on s2.product_id < s3.product_id 
    where s.receipt_id = s2.receipt_id and s2.receipt_id = s3.receipt_id 
        and s.receipt_id in (select id from receipts r where r."date">'{start_date.isoformat(sep=" ")}' and r."date"<'{end_date.isoformat(sep=" ")}')
    group by s.product_id ,s2.product_id , s3.product_id 
    order by number_of_sales desc
    fetch first 10 rows only;""")

    if 'column' in dbtype:
        statement = text(f"""
           select s.product_id as product_1, 
              s2.product_id as product_2, 
              s3.product_id as product_3,
              count(*) as number_of_sales, 
              LISTAGG(s.receipt_id, ',') as receipts
           from sales s join sales s2 on s.product_id < s2.product_id join sales s3 on s2.product_id < s3.product_id 
           where s.receipt_id = s2.receipt_id and s2.receipt_id = s3.receipt_id 
               and s.receipt_id in (select id from receipts r where r."date">TO_DATE('{start_date.date().isoformat()}','YYYY-MM-DD') and r."date"<TO_DATE('{end_date.date().isoformat()}','YYYY-MM-DD')  )
           group by s.product_id ,s2.product_id , s3.product_id 
           order by number_of_sales desc
           fetch first 10 rows only""")

    result_set = db.execute(statement)
    result = []
    for row in result_set:
        print(row)
        result.append(row)
    return result


# Вивести топ 10 купівель товарів по чотири за період С
@time_it.time_it_once(description="Порахувати вартість проданого товару за період")
def get_top10_4product_combinations_over_period(start_date: datetime, end_date: datetime, db: Session, dbtype="row"):
    statement = text(f"""
    select s.product_id as product_1, 
       s2.product_id as product_2, 
       s3.product_id as product_3,
       s4.product_id as product_4,
       count(*) as number_of_sales, 
       string_agg(s.receipt_id::varchar, ',') as receipts 
    from sales s join sales s2 on s.product_id < s2.product_id join sales s3 on s2.product_id < s3.product_id join sales s4 on s3.product_id < s4.product_id 
    where s.receipt_id = s2.receipt_id and s2.receipt_id = s3.receipt_id and s3.receipt_id = s4.receipt_id 
       and s.receipt_id in (select id from receipts r where r."date">'{start_date.isoformat(sep=" ")}' and r."date"<'{end_date.isoformat(sep=" ")}')
    group by s.product_id ,s2.product_id , s3.product_id , s4.product_id 
    order by number_of_sales desc
    fetch first 10 rows only;""")
    if 'column' in dbtype:
        statement = text(f"""
        select s.product_id as product_1, 
           s2.product_id as product_2, 
           s3.product_id as product_3,
           s4.product_id as product_4,
           count(*) as number_of_sales, 
           LISTAGG(s.receipt_id, ',') as receipts
        from sales s join sales s2 on s.product_id < s2.product_id join sales s3 on s2.product_id < s3.product_id join sales s4 on s3.product_id < s4.product_id 
        where s.receipt_id = s2.receipt_id and s2.receipt_id = s3.receipt_id and s3.receipt_id = s4.receipt_id 
           and s.receipt_id in (select id from receipts r where r."date">TO_DATE('{start_date.date().isoformat()}','YYYY-MM-DD')  and r."date"<TO_DATE('{end_date.date().isoformat()}','YYYY-MM-DD'))
        group by s.product_id ,s2.product_id , s3.product_id , s4.product_id 
        order by number_of_sales desc
        fetch first 10 rows only""")


    result_set = db.execute(statement)
    result = []
    for row in result_set:
        print(row)
        result.append(row)
    return result


