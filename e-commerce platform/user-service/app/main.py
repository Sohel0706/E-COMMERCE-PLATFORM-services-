from fastapi import FastAPI

from app.database.database import Base
from app.database.database import engine
from app.database.init_db import wait_for_db

app = FastAPI()


@app.on_event("startup")
def startup():

    wait_for_db()

    Base.metadata.create_all(bind=engine)
    
from app.api.user_routes import router

app = FastAPI(
    title="User Service"
)

app.include_router(router)


@app.get("/")
def health():
    return {
        "status": "running"
    }