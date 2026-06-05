import os

import httpx
from fastapi import HTTPException

from app.models.cart import CartItem

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")
PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://product-service:8000"
)


def create_cart_item(db, cart_item_data):
    user = fetch_user(cart_item_data.user_id)
    product = fetch_product(cart_item_data.product_id)

    cart_item = CartItem(
        user_id=cart_item_data.user_id,
        product_id=cart_item_data.product_id,
        quantity=cart_item_data.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return enrich_cart_item(cart_item, user, product)


def get_cart_items(db):
    return [
        enrich_cart_item(cart_item)
        for cart_item in db.query(CartItem).all()
    ]


def get_cart_item(db, cart_item_id):
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.id == cart_item_id)
        .first()
    )

    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return enrich_cart_item(cart_item)


def get_cart_items_by_user(db, user_id):
    user = fetch_user(user_id)
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .all()
    )

    return {
        "customer": user,
        "items": [
            enrich_cart_item(cart_item, user=user)
            for cart_item in cart_items
        ]
    }


def get_cart_items_by_product(db, product_id):
    product = fetch_product(product_id)
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.product_id == product_id)
        .all()
    )

    return {
        "product": product,
        "customers": [
            enrich_cart_item(cart_item, product=product)
            for cart_item in cart_items
        ]
    }


def enrich_cart_item(cart_item, user=None, product=None):
    if user is None:
        user = fetch_user(cart_item.user_id)

    if product is None:
        product = fetch_product(cart_item.product_id)

    return {
        "id": cart_item.id,
        "quantity": cart_item.quantity,
        "customer": user,
        "product": product
    }


def fetch_user(user_id):
    return fetch_service_resource(
        f"{USER_SERVICE_URL}/users/{user_id}",
        "User not found"
    )


def fetch_product(product_id):
    return fetch_service_resource(
        f"{PRODUCT_SERVICE_URL}/products/{product_id}",
        "Product not found"
    )


def fetch_service_resource(url, not_found_message):
    try:
        response = httpx.get(url, timeout=5.0)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Downstream service unavailable: {exc}"
        ) from exc

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=not_found_message)

    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail="Downstream service returned an error"
        )

    data = response.json()

    if data is None:
        raise HTTPException(status_code=404, detail=not_found_message)

    return data
