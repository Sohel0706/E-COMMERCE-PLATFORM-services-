import os

import httpx
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.database.dependencies import get_db
from app.services.user_service import (
    create_user,
    get_users,
    get_user
)

router = APIRouter()
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:8000")


@router.post("/users")
def create(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    return create_user(db, user)


@router.get("/users")
def list_users(
    db: Session = Depends(get_db)
):
    """Return all users."""
    return get_users(db)


@router.get("/users/{user_id}")
def fetch_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Return a user by their ID."""
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/users/{user_id}/cart")
def fetch_user_cart(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Return the cart items added by this user."""
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        response = httpx.get(
            f"{CART_SERVICE_URL}/carts/users/{user_id}",
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
