from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, Float, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, Sequence("shops_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return "<Shop(id='%s', name='%s')>" % (
            self.id,
            self.name,
        )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Sequence("products_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return "<Product(id='%s', name='%s', price='%s')>" % (
            self.id,
            self.name,
            self.price
        )


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, Sequence("receipts_id_seq"), primary_key=True)
    total_price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    # many-to-one
    shop_id = Column(Integer, ForeignKey("shops.id"))
    shop = relationship("Shop")

    sales = relationship("Sale")

    def __repr__(self):
        return "<Receipt(id='%s', total_price='%s', date='%s', shop_id='%s')>" % (
            self.id,
            self.total_price,
            self.date,
            self.shop_id
        )


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, Sequence("sales_id_seq"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # many-to-one
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product")

    receipt_id = Column(Integer, ForeignKey("receipts.id"))

    def __repr__(self):
        return "<Sale(id='%s', quantity='%s', price='%s', product_id='%s', receipt_id='%s')>" % (
            self.id,
            self.quantity,
            self.price,
            self.product_id,
            self.receipt_id
        )