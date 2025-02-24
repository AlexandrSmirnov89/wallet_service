from fastapi import FastAPI
from src.api.v1.endpoints.wallet import router as wallet_router

app = FastAPI(
    title="Wallet API",
    description="API для управления балансом кошельков",
    version="1.0.0",
)

app.include_router(wallet_router, prefix="/api/v1", tags=["Wallets"])

@app.get("/")
async def root():
    return {"message": "Wallet API is running"}
