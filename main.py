import sys

from fastapi import FastAPI, Depends, HTTPException
from models import Base
from column_oriented.database import oracle_engine, OracleSession
from row_oriented.database import postgres_engine, PostgresSession
import schemas
import queries
import advanced_queries
from sqlalchemy.orm import Session

# Creating tables for each database
Base.metadata.create_all(oracle_engine)
Base.metadata.create_all(postgres_engine)

app = FastAPI()


# Dependency
def get_postgres_db():
    db = PostgresSession()
    try:
        yield db
    finally:
        db.close()


def get_oracle_db():
    db = OracleSession()
    try:
        yield db
    finally:
        db.close()


def get_db(db_type):
    if "column" in db_type:
        return OracleSession()
    elif "row" in db_type:
        return PostgresSession()
    else:
        print("Wrong db-type value: ", db_type)
        sys.exit(1)


# Shop
@app.post("/shop", response_model=schemas.Shop)
def create_shop(db_type: str, shop: schemas.ShopCreate):
    db = get_db(db_type)
    data = queries.create_shop(db=db, shop=shop)
    db.close()
    return data


@app.get("/shop", response_model=list[schemas.Shop])
def get_shops(db_type: str, skip: int = 0, limit: int = 100):
    db = get_db(db_type)
    organizations = queries.get_shops(db, skip=skip, limit=limit)
    db.close()
    return organizations


@app.get("/shop/{shop_id}", response_model=schemas.Shop)
def get_shop_by_id(db_type: str, shop_id: int):
    db = get_db(db_type)
    entity = queries.get_shop_by_id(db, shop_id=shop_id)
    db.close()
    if entity is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return entity


# Product

@app.post("/product", response_model=schemas.Product)
def create_product(db_type: str, product: schemas.ProductCreate):
    db = get_db(db_type)
    entity = queries.get_product_by_name(db, name=product.name)
    if entity:
        db.close()
        raise HTTPException(status_code=409, detail="Entity with such name already exists")
    product = queries.create_product(db=db, product=product)
    db.close()
    return product


@app.get("/product", response_model=list[schemas.Product])
def get_products(db_type: str, skip: int = 0, limit: int = 100):
    db = get_db(db_type)
    products = queries.get_products(db, skip=skip, limit=limit)
    db.close()
    return products


@app.get("/product/{product_id}", response_model=schemas.Product)
def get_product_by_id(db_type: str, product_id: int):
    db = get_db(db_type)
    entity = queries.get_product_by_id(db, product_id=product_id)
    db.close()
    if entity is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return entity


# Receipt

@app.post("/receipt", response_model=schemas.Receipt)
def create_receipt(db_type: str, receipt: schemas.ReceiptCreate):
    db = get_db(db_type)
    receipt = queries.create_receipt(db=db, receipt=receipt)
    db.close()
    return receipt


@app.get("/receipt", response_model=list[schemas.Receipt])
def get_receipts(db_type: str, skip: int = 0, limit: int = 100):
    db = get_db(db_type)
    receipts = queries.get_receipts(db, skip=skip, limit=limit)
    db.close()
    return receipts


@app.get("/receipt/{receipt_id}", response_model=schemas.Receipt)
def get_receipt_by_id(db_type: str, receipt_id: int):
    db = get_db(db_type)
    entity = queries.get_receipt_by_id(db, receipt_id=receipt_id)
    db.close()
    if entity is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return entity


# Sale

@app.post("/sale", response_model=schemas.Sale)
def create_sale(db_type: str, sale: schemas.SaleCreate):
    db = get_db(db_type)
    response = queries.create_sale(db=db, sale=sale)
    db.close()
    return response


@app.get("/sale", response_model=list[schemas.Sale])
def get_sales(db_type: str, skip: int = 0, limit: int = 100):
    db = get_db(db_type)
    receipts = queries.get_sales(db, skip=skip, limit=limit)
    db.close()
    return receipts


@app.get("/sale/{sale_id}", response_model=schemas.Sale)
def get_sale_by_id(db_type: str, sale_id: int):
    db = get_db(db_type)
    entity = queries.get_sale_by_id(db, sale_id=sale_id)
    db.close()
    if entity is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return entity


@app.get("/total_sold_quantity_by_product")
def get_total_sold_quantity_by_product(db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_total_sold_quantity_by_product(db)
    db.close()
    return result


@app.get("/total_sold_price_by_product")
def get_total_sold_price_by_product(db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_total_sold_price_by_product(db)
    db.close()
    return result


@app.put("/total_sold_price_by_product_over_period")
def get_total_sold_price_by_product_over_period(period: schemas.Period, db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_total_sold_price_by_product_over_period(db=db, start_date=period.start_date,
                                                                          end_date=period.end_date)
    db.close()
    return result


@app.put("/product_quantity_in_shop_over_period")
def get_product_quantity_in_shop_over_period(period: schemas.ProductShopPeriod, db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_product_quantity_in_shop_over_period(db=db, start_date=period.start_date,
                                                                       end_date=period.end_date,
                                                                       product_id=period.product_id,
                                                                       shop_id=period.shop_id)
    db.close()
    return result


@app.put("/product_quantity_in_all_shops_over_period")
def get_product_quantity_in_all_shops_over_period(period: schemas.ProductPeriod, db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_product_quantity_in_all_shops_over_period(db=db, start_date=period.start_date,
                                                                            end_date=period.end_date,
                                                                            product_id=period.product_id)
    db.close()
    return result


@app.put("/total_revenue_over_period")
def get_total_revenue_over_period(period: schemas.Period, db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_total_revenue_over_period(db=db, start_date=period.start_date,
                                                            end_date=period.end_date)
    db.close()
    return result


@app.put("/top10_2product_combinations_over_period")
def get_top10_2product_combinations_over_period(period: schemas.Period, db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_top10_2product_combinations_over_period(db=db, start_date=period.start_date,
                                                                          end_date=period.end_date)
    db.close()
    return result


@app.put("/top10_3product_combinations_over_period")
def get_top10_3product_combinations_over_period(period: schemas.Period, db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_top10_3product_combinations_over_period(db=db, start_date=period.start_date,
                                                                          end_date=period.end_date)
    db.close()
    return result


@app.put("/top10_4product_combinations_over_period")
def get_top10_4product_combinations_over_period(period: schemas.Period, db_type: str):
    db = get_db(db_type)
    result = advanced_queries.get_top10_4product_combinations_over_period(db=db, start_date=period.start_date,
                                                                          end_date=period.end_date)
    db.close()
    return result


@app.get("/")
async def root():
    return {"message": "Hello World"}
