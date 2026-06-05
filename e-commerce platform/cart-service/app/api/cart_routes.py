from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.cart import CartItemCreate
from app.services.cart_service import (
    create_cart_item,
    get_cart_item,
    get_cart_items,
    get_cart_items_by_product,
    get_cart_items_by_user,
)

router = APIRouter()


@router.post("/cart-items")
def create(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db)
):
    """Add a product to a customer's cart."""
    return create_cart_item(db, cart_item)


@router.get("/cart-items")
def list_cart_items(
    db: Session = Depends(get_db)
):
    """Return all cart items with customer and product details."""
    return get_cart_items(db)


@router.get("/cart-items/{cart_item_id}")
def fetch_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db)
):
    """Return one cart item by its ID with customer and product details."""
    return get_cart_item(db, cart_item_id)


@router.get("/carts/users/{user_id}")
def fetch_user_cart(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Return the cart items added by a specific customer."""
    return get_cart_items_by_user(db, user_id)


@router.get("/carts/products/{product_id}")
def fetch_product_cart_customers(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Return the customers who added a specific product to their cart."""
    return get_cart_items_by_product(db, product_id)
