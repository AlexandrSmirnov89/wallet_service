from pydantic import BaseModel, UUID4, condecimal, ConfigDict
from enum import Enum

class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletCreate(BaseModel):
    balance: condecimal(ge=0, decimal_places=2) = 0
    model_config = ConfigDict(from_attributes=True)

class WalletOperation(BaseModel):
    operationType: OperationType
    amount: condecimal(gt=0, decimal_places=2)
    model_config = ConfigDict(from_attributes=True)

class WalletResponse(BaseModel):
    id: UUID4
    balance: condecimal(decimal_places=2)
    model_config = ConfigDict(from_attributes=True)
