from decimal import Decimal
import pytest
from transaction_processor.processor import process_transaction, get_balance
from transaction_processor.models import Transaction
from transaction_processor.errors import DuplicateTransactionError, OverdraftError

def test_process_transaction_duplicate():
    ledger = [Transaction("1", Decimal("100"), "CREDIT", "a")]
    tx = Transaction("1", Decimal("50"), "CREDIT", "a")  
    with pytest.raises(DuplicateTransactionError):
        process_transaction(tx, ledger)

def test_process_transaction_overdraft():
    ledger = [Transaction("1", Decimal("50"), "CREDIT", "a")]
    tx = Transaction("1", Decimal("100"), "DEBIT", "b")  
    with pytest.raises(OverdraftError):
        process_transaction(tx, ledger)

def test_process_transaction_exact_debit():
    ledger = [Transaction("1", Decimal("50"), "CREDIT", "a")]
    tx = Transaction("1", Decimal("50"), "DEBIT", "b")  
    process_transaction(tx, ledger)
    assert get_balance("1", ledger) == Decimal("0")

from decimal import Decimal
from transaction_processor.models import Transaction
from transaction_processor.processor import get_balance, process_transaction

def test_multiple_credits_balance():
    ledger = [
        Transaction(account_id="1", type="CREDIT", amount=Decimal("100"), idempotency_key="a"),
        Transaction(account_id="1", type="CREDIT", amount=Decimal("50"), idempotency_key="b"),
        Transaction(account_id="1", type="CREDIT", amount=Decimal("25"), idempotency_key="c"),
    ]
    assert get_balance("1", ledger) == Decimal("175")

def test_multiple_debits_balance():
    ledger = [
        Transaction(account_id="1", type="CREDIT", amount=Decimal("200"), idempotency_key="a"),
        Transaction(account_id="1", type="DEBIT", amount=Decimal("50"), idempotency_key="b"),
        Transaction(account_id="1", type="DEBIT", amount=Decimal("25"), idempotency_key="c"),
    ]
    assert get_balance("1", ledger) == Decimal("125")
