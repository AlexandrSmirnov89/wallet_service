from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from src.models.wallet import Wallet
from sqlalchemy.orm import Session


class WalletRepository:
    @staticmethod
    async def get_wallet(wallet_id: str, db: AsyncSession, for_update: bool = False):
        query = select(Wallet).where(Wallet.id == wallet_id)
        if for_update:
            query = query.with_for_update(skip_locked=True)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_wallet(db: AsyncSession, balance: Decimal = 0):
        wallet = Wallet(balance=balance)
        db.add(wallet)
        await db.commit()
        await db.refresh(wallet)
        return wallet

    @staticmethod
    async def update_balance(wallet: Wallet, amount: float, db: AsyncSession):
        wallet.balance += amount
        await db.commit()
        await db.refresh(wallet)
        return wallet

    @staticmethod
    async def delete_wallet(wallet_id: str, db: AsyncSession):
        wallet = await WalletRepository.get_wallet(wallet_id, db)
        if wallet:
            await db.delete(wallet)
            await db.commit()
            return True
        return False

    @staticmethod
    def delete_wallet_sync(wallet_id: str, db: Session):
        wallet = WalletRepository.get_wallet_sync(wallet_id, db)
        if wallet:
            db.delete(wallet)
            db.commit()
            return True
        return False

    @staticmethod
    def get_wallet_sync(wallet_id: str, db: Session, for_update: bool = False):
        query = select(Wallet).where(Wallet.id == wallet_id)
        if for_update:
            query = query.with_for_update()
        return db.execute(query).scalars().first()

    @staticmethod
    def update_balance_sync(wallet: Wallet, amount: float, db: Session):
        wallet.balance += Decimal(str(amount))
        db.commit()
        db.refresh(wallet)
        return wallet