import pytest
from main.validator import Validator  # Correct import for Validator class
from decimal import Decimal
import re

@pytest.fixture
def validator_setup():
    return Validator()


def test_account_number_valid(validator_setup):
    valid_account_number = "ACC12345"
    result = validator_setup.account_number_validation(valid_account_number)
    assert result == valid_account_number


def test_account_number_empty(validator_setup):
    with pytest.raises(ValueError, match="Account number cannot be empty"):
        validator_setup.account_number_validation("")


def test_account_number_invalid_format(validator_setup):
    with pytest.raises(ValueError, match=re.escape("Account number must be ACC + digits (e.g., ACC001)")):
        validator_setup.account_number_validation("12345")

def test_account_name_valid(validator_setup):
    valid_name = "John Doe"
    result = validator_setup.account_name_validation(valid_name)
    assert result == valid_name

def test_account_name_validation_empty(validator_setup):
    with pytest.raises(ValueError, match="Account name cannot be empty."):
        validator_setup.account_name_validation("")

def test_account_name_validation_too_short(validator_setup):
    with pytest.raises(ValueError, match="Account name must be at least 3 characters long."):
        validator_setup.account_name_validation("Jo")

# Test amount validation
def test_amount_validation_valid(validator_setup):
    valid_amount = 100.5
    result = validator_setup.amount_validation(valid_amount)
    assert result == Decimal("100.5")

def test_amount_validation_zero(validator_setup):
    with pytest.raises(ValueError, match="Amount must be greater than zero"):
        validator_setup.amount_validation(0)

def test_amount_validation_negative(validator_setup):
    with pytest.raises(ValueError, match="Amount must be greater than zero"):
        validator_setup.amount_validation(-50)