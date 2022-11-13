from fastapi import FastAPI, Depends, HTTPException
from models import Base
from column_oriented.database import oracle_engine, OracleSession
from row_oriented.database import postgres_engine, PostgresSession
import schemas
import queries
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


# Shop
@app.post("/shop", response_model=schemas.Shop)
def create_shop(shop: schemas.ShopCreate, db: Session = Depends(get_postgres_db)):
    entity = queries.get_shop_by_name(db, name=shop.name)
    if entity:
        raise HTTPException(status_code=409, detail="Entity with such name already exists")
    return queries.create_shop(db=db, shop=shop)


@app.get("/shop", response_model=list[schemas.Shop])
def get_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_db)):
    organizations = queries.get_shops(db, skip=skip, limit=limit)
    return organizations


@app.get("/shop/{shop_id}", response_model=schemas.Shop)
def get_shop_by_id(shop_id: int, db: Session = Depends(get_postgres_db)):
    entity = queries.get_shop_by_id(db, shop_id=shop_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return entity


# Product

@app.post("/product", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_postgres_db)):
    entity = queries.get_product_by_name(db, name=product.name)
    if entity:
        raise HTTPException(status_code=409, detail="Entity with such name already exists")
    return queries.create_product(db=db, product=product)


@app.get("/product", response_model=list[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_db)):
    products = queries.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/product/{product_id}", response_model=schemas.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_postgres_db)):
    entity = queries.get_product_by_id(db, product_id=product_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return entity


# Receipt

@app.post("/receipt", response_model=schemas.Receipt)
def create_receipt(receipt: schemas.ReceiptCreate, db: Session = Depends(get_postgres_db)):
    return queries.create_receipt(db=db, receipt=receipt)


@app.get("/receipt", response_model=list[schemas.Receipt])
def get_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_db)):
    receipts = queries.get_receipts(db, skip=skip, limit=limit)
    return receipts


@app.get("/receipt/{receipt_id}", response_model=schemas.Receipt)
def get_receipt_by_id(receipt_id: int, db: Session = Depends(get_postgres_db)):
    entity = queries.get_receipt_by_id(db, receipt_id=receipt_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return entity


# Sale

@app.post("/sale", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_postgres_db)):
    return queries.create_sale(db=db, sale=sale)


@app.get("/sale", response_model=list[schemas.Sale])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_db)):
    receipts = queries.get_sales(db, skip=skip, limit=limit)
    return receipts


@app.get("/sale/{sale_id}", response_model=schemas.Sale)
def get_sale_by_id(sale_id: int, db: Session = Depends(get_postgres_db)):
    entity = queries.get_sale_by_id(db, sale_id=sale_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return entity


#


@app.get("/")
async def root():
    return {"message": "Hello World"}
