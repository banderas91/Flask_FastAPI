
import datetime
from typing import List

from fastapi import FastAPI, logger
from pydantic import BaseModel, EmailStr

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


import logging

logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()

engine = create_engine("sqlite:///test.db")
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class Product(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int

    class Config:
        from_attributes = True


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


class ProductTable(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)


class OrderTable(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))


Base.metadata.create_all(engine)

session = Session()


@app.post("/users", response_model=User)
def create_user(user: User):

    logger.info("Создание пользователя %s", user)

    try:
        user_ids = [u.id for u in get_users()]
        logger.info("Список ID пользователей: %s", user_ids)

        new_id = 1
        if user_ids:
            new_id = max(user_ids) + 1

        logger.info("Новый ID пользователя: %s", new_id)

        new_user = UserTable(
            id=new_id,
            name=user.name,
            email=user.email
        )

        logger.info("Сохранение нового пользователя %s", new_user)

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    except Exception as e:
        logger.exception("Ошибка создания пользователя:")
        raise e

    return new_user


@app.get("/users", response_model=List[User])
def get_users():
    return session.query(UserTable).all()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    return session.query(UserTable).get(user_id)


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    db_user = session.query(UserTable).get(user_id)
    db_user.name = user.name
    db_user.email = user.email
    session.commit()
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db_user = session.query(UserTable).get(user_id)
    session.delete(db_user)
    session.commit()
    return {"ok": True}


# CRUD для продуктов

@app.post("/products", response_model=Product)
def create_product(product: Product):
    db_product = ProductTable(
        name=product.name,
        description=product.description,
        price=product.price
    )
    session.add(db_product)
    session.commit()
    return db_product


@app.get("/products", response_model=List[Product])
def read_products():
    return session.query(ProductTable).all()


@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    return session.query(ProductTable).get(product_id)


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    db_prod = session.query(ProductTable).get(product_id)
    db_prod.name = product.name
    db_prod.description = product.description
    db_prod.price = product.price
    session.commit()
    return db_prod


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db_prod = session.query(ProductTable).get(product_id)
    session.delete(db_prod)
    session.commit()
    return {"ok": True}


# CRUD для заказов

@app.post("/orders", response_model=Order)
def create_order(order: Order):
    db_order = OrderTable(
        user_id=order.user_id,
        product_id=order.product_id,
        order_date=datetime.now(),
        status="new"
    )
    session.add(db_order)
    session.commit()
    return db_order


@app.get("/orders", response_model=List[Order])
def read_orders():
    return session.query(OrderTable).all()


@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int):
    return session.query(OrderTable).get(order_id)


@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: Order):
    db_order = session.query(OrderTable).get(order_id)
    db_order.user_id = order.user_id
    db_order.product_id = order.product_id
    session.commit()
    return db_order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    db_order = session.query(OrderTable).get(order_id)
    session.delete(db_order)
    session.commit()
    return {"ok": True}


# Пример тестовых данных
product1 = ProductTable(name="iPhone_13", price=1000)
session.add(product1)

user1 = UserTable(name="Petr", email="petr@example.com")
session.add(user1)

order1 = OrderTable(user_id=user1.id, product_id=product1.id)
session.add(order1)

session.commit()


