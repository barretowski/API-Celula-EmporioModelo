from fastapi import FastAPI
from routes import users
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/usario", tags=["usuario"])