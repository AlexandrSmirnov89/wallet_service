from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.cache_redis import get_async_cache
from src.core.db import get_db
from src.schemas.wallet import WalletOperation, WalletResponse, WalletCreate
from src.services.wallet import WalletService
from src.api.v1.tasks import process_wallet_operation, get_wallet_balance_task

router = APIRouter()

@router.post("/wallets/", response_model=WalletResponse)
async def create_wallet(wallet_data: WalletCreate, db: AsyncSession = Depends(get_db)):
    wallet = await WalletService.create_wallet(wallet_data, db)
    return WalletResponse(id=wallet.id, balance=wallet.balance)

@router.post("/wallets/{wallet_id}/operation", status_code=202)
async def wallet_operation(wallet_id: str, operation: WalletOperation):
    task = process_wallet_operation.delay(wallet_id, operation.operationType.value, float(operation.amount))
    result = task.get(timeout=5)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/wallets/{wallet_id}")
async def get_wallet_balance(wallet_id: str):
    cached_balance = await get_async_cache(wallet_id)
    if cached_balance is not None:
        return {"wallet_id": wallet_id, "balance": cached_balance}

    task = get_wallet_balance_task.delay(wallet_id)
    result = task.get(timeout=5)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.delete("/wallets/{wallet_id}", status_code=204)
async def delete_wallet(wallet_id: str, db: AsyncSession = Depends(get_db)):
    try:
        await WalletService.delete_wallet(wallet_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Wallet not found")