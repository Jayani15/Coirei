from fastapi import FastAPI
from .database import engine, Base
from .routers import products

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Management API")

app.include_router(products.router)

@app.get("/health")
def health_check():
    return {"status": "API is running"}
