from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.models.product import Product

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(payload:ProductCreate, db:Session=Depends(get_db)):
    existing_product = db.query(Product).filter(
        Product.name == payload.name
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product name already exists"
        )

    new_product = Product(
        name=payload.name,
        brand=payload.brand,
        model_number=payload.model_number,
        category=payload.category
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ProductResponse])
def get_products(db:Session=Depends(get_db)):
    statement=select(Product)
    results = db.execute(statement)
    products = results.scalars().all()
    return products

@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def get_product(product_id:int, db:Session=Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.patch("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def update_product(product_id:int, payload:ProductUpdate, db:Session=Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    if payload.name is not None:
        existing_product=db.query(Product).filter(
            Product.name == payload.name
        ).first()
        if existing_product and existing_product.id != product.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists"
            )
    updated_values = payload.model_dump(exclude_unset=True)
    for field, value in updated_values.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_product(product_id, db:Session=Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    db.delete(product)
    db.commit()
    return {"msg":"product deleted successfully"}



