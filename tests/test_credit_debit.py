from transaction_processor.models import Transaction
from decimal import Decimal
from transaction_processor.processor import get_balance

def test_get_balance_credit_and_debit():
    ledger = [
        Transaction(account_id="1", type="CREDIT", amount=Decimal("100"), idempotency_key="a"),
        Transaction(account_id="1", type="DEBIT",  amount=Decimal("40"),  idempotency_key="b"),
    ]
    assert get_balance("1", ledger) == Decimal("60")
