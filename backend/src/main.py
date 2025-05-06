# src/main.py
from fastapi import FastAPI
from src.api.contracts import router as contracts_router
from src.database import init_db

app = FastAPI(title="DeFi Analyzer API")
app.include_router(contracts_router)

@app.get("/")
async def root():
    return {"message": "DeFi Analyzer API is running"}

@app.on_event("startup")
async def startup_event():
    await init_db()