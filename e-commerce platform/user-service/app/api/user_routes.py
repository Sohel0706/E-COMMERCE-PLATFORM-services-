from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.database.dependencies import get_db
from app.services.user_service import (
    create_user,
    get_users,
    get_user
)

router = APIRouter()


@router.post("/users")
def create(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)


@router.get("/users")
def list_users(
    db: Session = Depends(get_db)
):
    return get_users(db)


@router.get("/users/{user_id}")
def fetch_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user(db, user_id)