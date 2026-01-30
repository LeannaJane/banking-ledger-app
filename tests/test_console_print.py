import io
import sys
from transaction_processor.processor import print_ledger
from decimal import Decimal

def test_print_ledger(capsys):
    from transaction_processor.models import Transaction
    ledger = [
        Transaction(account_id="1", type="CREDIT", amount=Decimal("100"), idempotency_key="a"),
        Transaction(account_id="1", type="CREDIT", amount=Decimal("50"), idempotency_key="b"),
        Transaction(account_id="1", type="CREDIT", amount=Decimal("25"), idempotency_key="c"),
    ]
    print_ledger(ledger)
    captured = capsys.readouterr().out
    assert "1" in captured
    assert "2" in captured
    assert "100" in captured
    assert "50" in captured
