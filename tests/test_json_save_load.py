import pytest
from decimal import Decimal
from transaction_processor.processor import save_ledger, load_ledger
from transaction_processor.models import Transaction
from transaction_processor.processor import get_balance

def test_save_and_load_ledger(tmp_path):
    ledger = [
        Transaction("1", Decimal("100"), "CREDIT", "a"),
        Transaction("1", Decimal("40"), "DEBIT", "b")
    ]
    file = tmp_path / "ledger.json"
    save_ledger(ledger, filename=file)
    loaded_ledger = load_ledger(filename=file)
    assert len(loaded_ledger) == 2
    assert sum(tx.amount for tx in loaded_ledger if tx.type=="CREDIT") == Decimal("100")
    assert sum(tx.amount for tx in loaded_ledger if tx.type=="DEBIT") == Decimal("40")

def test_load_corrupt_json(tmp_path):
    file = tmp_path / "ledger.json"
    file.write_text("{ this is not json }")
    ledger = load_ledger(filename=file)
    assert ledger == []

def test_get_balance_empty_ledger():
    assert get_balance("1", []) == Decimal("0")
