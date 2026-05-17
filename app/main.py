from fastapi import FastAPI
from app.init_db import init_db
from app.api.routes import item , item_images, auth, users 
from fastapi.staticfiles import StaticFiles
from app.core.config import UPLOAD_DIR, STATIC_URL

app = FastAPI()

app.include_router(item.router)
app.include_router(item_images.router)
app.include_router(auth.router)
app.include_router(users.router)
app.mount(STATIC_URL, StaticFiles(directory=UPLOAD_DIR), name="static")

@app.on_event("startup")
def on_startup():
    init_db()


