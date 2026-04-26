from fastapi import FastAPI
from init_db import init_db
from api.routes import item

app = FastAPI()


app.include_router(item.router)

@app.on_event("startup")
def on_startup():
    init_db()


