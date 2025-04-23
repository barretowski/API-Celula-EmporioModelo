from fastapi import FastAPI
from routes.usuario import router
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/usuario", tags=["usuario"])