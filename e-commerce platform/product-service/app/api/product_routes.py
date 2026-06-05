import os

import httpx
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.product import ProductCreate
from app.services.product_service import (
    create_product,
    get_product,
    get_products,
)

router = APIRouter()
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:8000")


@router.post("/products")
def create(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product."""
    return create_product(db, product)


@router.get("/products")
def list_products(
    db: Session = Depends(get_db)
):
    """Return all products."""
    return get_products(db)


@router.get("/products/{product_id}")
def fetch_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Return a product by its ID."""
    product = get_product(db, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.get("/products/{product_id}/carts")
def fetch_product_cart_customers(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Return customers who added this product to their cart."""
    product = get_product(db, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        response = httpx.get(
            f"{CART_SERVICE_URL}/carts/products/{product_id}",
            timeout=5.0
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Cart service unavailable: {exc}"
        ) from exc

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )

    return response.json()
