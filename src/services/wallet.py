from http.client import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.wallet import WalletRepository
from src.schemas.wallet import WalletCreate, WalletOperation, OperationType


class WalletService:
    @staticmethod
    async def create_wallet(wallet_data: WalletCreate, db: AsyncSession):
        if wallet_data.balance < 0:
            raise HTTPException(
                status_code=400,
                detail="Balance cannot be negative"
            )
        return await WalletRepository.create_wallet(db, balance=wallet_data.balance)

    @staticmethod
    async def delete_wallet(wallet_id: str, db: AsyncSession):
        success = await WalletRepository.delete_wallet(wallet_id, db)
        if not success:
            raise ValueError("Wallet not found")
