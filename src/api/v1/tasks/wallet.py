from decimal import Decimal

from src.cache.cache_redis import set_cache
from src.core.celery_config import celery_app
from src.repositories.wallet import WalletRepository
from src.core.db import get_sync_db
from src.schemas.wallet import OperationType


@celery_app.task
def process_wallet_operation(wallet_id: str, operation_type: str, amount: float):
    db = get_sync_db()
    try:
        wallet = WalletRepository.get_wallet_sync(wallet_id, db, for_update=True)
        if not wallet:
            return {"error": "Wallet not found"}

        if operation_type == OperationType.WITHDRAW and wallet.balance < amount:
            return {"error": "Insufficient funds"}

        updated_wallet = WalletRepository.update_balance_sync(
            wallet, amount
            if operation_type == OperationType.DEPOSIT
            else -Decimal(str(amount)), db
        )

        import asyncio
        asyncio.run(set_cache(wallet_id, updated_wallet.balance))

        return {"wallet_id": wallet.id, "balance": str(updated_wallet.balance)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


@celery_app.task
def get_wallet_balance_task(wallet_id: str):
    db = get_sync_db()
    try:
        wallet = WalletRepository.get_wallet_sync(wallet_id, db)
        if not wallet:
            return {"error": "Wallet not found!"}

        import asyncio
        asyncio.run(set_cache(wallet_id, float(wallet.balance)))

        return {"wallet_id": wallet.id, "balance": str(wallet.balance)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
