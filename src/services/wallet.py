import uuid
from unicodedata import decimal

from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.wallet import WalletRepository
from src.schemas.wallet import WalletCreate, WalletOperation, OperationType


class WalletService:
    @staticmethod
    async def create_wallet(wallet_data: WalletCreate, db: AsyncSession):
        return await WalletRepository.create_wallet(db, balance=wallet_data.balance)

    @staticmethod
    async def delete_wallet(wallet_id: str, db: AsyncSession):
        success = await WalletRepository.delete_wallet(wallet_id, db)
        if not success:
            raise ValueError("Wallet not found")


# class WalletService:
#     @staticmethod
#     @celery_task
#     async def process_operation(wallet_id: str, operation: WalletOperation, db: AsyncSession):
#         async with db.begin():  # Начинаем транзакцию
#             wallet = await WalletRepository.get_wallet(wallet_id, db, for_update=True)
#             if not wallet:
#                 raise ValueError("Wallet not found")
#
#             if operation.operationType == OperationType.WITHDRAW and wallet.balance < operation.amount:
#                 raise ValueError("Insufficient funds")
#
#             return await WalletRepository.update_balance(wallet, operation.amount if operation.operationType == OperationType.DEPOSIT else -operation.amount, db)
#
#     @staticmethod
#     @celery_task
#     async def create_wallet(wallet_data: WalletCreate, db: AsyncSession):
#         wallet_id = str(uuid.uuid4())  # Генерируем UUID
#         return await WalletRepository.create_wallet(wallet_id, wallet_data.balance, db)
#
#     @staticmethod
#     @celery_task
#     async def delete_wallet(wallet_id: str, db: AsyncSession):
#         success = await WalletRepository.delete_wallet(wallet_id, db)
#         if not success:
#             raise ValueError("Wallet not found")