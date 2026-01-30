from decimal import Decimal
from transaction_processor.processor import get_balance
from transaction_processor.models import Transaction

def test_get_balance_single_credit():
    ledger = [
        Transaction(
            account_id="1",
            type="CREDIT",
            amount=Decimal("100"),
            idempotency_key="abc",
        )
    ]

    assert get_balance("1", ledger) == Decimal("100")


def test_get_balance_multiple_accounts():
    ledger = [
        Transaction(account_id="1", type="CREDIT", amount=Decimal("100"), idempotency_key="a"),
        Transaction(account_id="2", type="CREDIT", amount=Decimal("50"), idempotency_key="b"),
    ]
    assert get_balance("1", ledger) == Decimal("100")
    assert get_balance("2", ledger) == Decimal("50")
