DATABASE_URL = (
    "mysql+pymysql://root:root@localhost/users"
)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}