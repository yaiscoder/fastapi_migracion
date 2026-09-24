from fastapi import Depends, FastAPI, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field
from sqlmodel import select
from src.models.product_model import Product, ProductCategories
from src.shared.database.session_db import SessionDep, get_session

app = FastAPI()

class CreateProduct(BaseModel):
    name: str
    price: Annotated[float, Field(gt=10000)]
    quantity: Annotated[int,Field(ge=0)]
    category: ProductCategories

class UpdateProduct(BaseModel):
    name: str | None = None
    price: Annotated[float, Field(gt=10000)] | None = None
    quantity: Annotated[int, Field(ge=0)] | None = None
    category: ProductCategories | None = None

@app.post("/product")
def create_product(product: CreateProduct, session: SessionDep):
    if create_product:
        product = Product(name = product.name, category= product.category, price=product.price, quantity=product.quantity)
        session.add(product)
        session.commit()
        session.refresh(product)
        raise HTTPException(status_code=201, detail="Product successfully saved")
    return product

@app.put('/product/{product_id}')
def update_product(product_id: int, product: UpdateProduct, session: SessionDep):
    db_product = session.exec(
        select(Product).where(Product.id == product_id)
    ).one()
 
    product_data = product.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
 
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.get("/product")
def get_products(session: SessionDep):
    products = session.exec(
        select(Product)
    ).all()

    return products

@app.delete('/product/{id}')
def delete_product(product_id: int, session: SessionDep):
    product = session.exec(
            select(Product).where(Product.id == product_id)
    ).one()
    session.delete(product)
    session.commit()