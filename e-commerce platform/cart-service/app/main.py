from fastapi import FastAPI

from app.api.cart_routes import router
from app.database.database import Base
from app.database.database import engine
from app.database.init_db import wait_for_db

app = FastAPI(
    title="Cart Service"
)


@app.on_event("startup")
def startup():
    wait_for_db()
    Base.metadata.create_all(bind=engine)


app.include_router(router)


@app.get("/")
def health():
    return {
        "status": "running"
    }
