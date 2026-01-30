import pytest
from decimal import Decimal
from transaction_processor.processor import validate_amount

def test_validate_amount_zero():
    with pytest.raises(ValueError, match="greater than 0"):
        validate_amount("0")

def test_validate_amount_negative():
    with pytest.raises(ValueError, match="greater than 0"):
        validate_amount("-50")

def test_validate_amount_non_numeric():
    with pytest.raises(ValueError, match="number"):
        validate_amount("abc")

def test_validate_amount_valid():
    assert validate_amount("100") == Decimal("100")
