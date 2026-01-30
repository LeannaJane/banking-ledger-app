from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Transaction:
    account_id: str
    amount: Decimal
    type: str
    idempotency_key: str
    