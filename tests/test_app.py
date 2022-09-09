from audioop import mul
import pytest
from app.calculations import multiply, BankAccount, InsufficientFunds

# use a fixture when multiply tests use the same variables
@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("x, y, z", [
    (3, 4, 12),
    (5, 6, 30),
    (7, 8, 56)])
def test_multiply(x, y, z):
    assert multiply(x, y) == z

# the fixture is a function, the output of which, when plugged into a test, gets stored as a variable with the same name
def test_bank_set_initial_amount(bank_account):
    #bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_deposit(bank_account):
    #bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_bank_deposit(bank_account):
    #bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (150, 100, 100),
    (50, 100, 0),
    (1000, 150, 900)])
def test_bank_transactions(bank_account, deposited, withdrawn, expected):
    bank_account.deposit(deposited)
    bank_account.withdraw(withdrawn)
    assert bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(100)
