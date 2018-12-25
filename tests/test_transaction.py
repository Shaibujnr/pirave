import pytest
from pirave.response import Response
from pirave.enums import RESPONSE_STATUS, TRANSACTION_STATUS, CHARGE, SUGGESTED_AUTH
from pirave.transaction import Transaction
from pirave.exceptions import TrasactionNotFoundError, InvalidChargeTypeError


def test_verify_transaction_with_txref(api):
    txref = "712480329"
    response = Transaction.verify(txref)
    assert response == TRANSACTION_STATUS.PENDING


def test_verify_transaction_with_flwref(api):
    flwref = "FLW-MOCK-bda70b433a1fdb577dbb880ae1ee37b2"
    response = Transaction.verify(None, flwref)
    assert response == TRANSACTION_STATUS.SUCCESS


def test_verify_transaction_with_flwref_and_txref(api):
    txref = "712480329"
    flwref = "FLW-MOCK-bda70b433a1fdb577dbb880ae1ee37b2"
    with pytest.raises(TrasactionNotFoundError):
        Transaction.verify(txref,flwref)


def test_get_transaction_with_txref(api):
    txref = "41235"
    transaction = Transaction.get(txref)
    assert transaction is not None
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.SUCCESS
    assert transaction.txref == txref
    assert transaction.amount == 5000
    assert transaction.rave_fee == 70


def test_get_transaction_with_flwref(api):
    flwref = "FLW-MOCK-f3a83d622bc3bbc7f21f2f0e7c6627cd"
    transaction = Transaction.get(None, flwref)
    assert transaction is not None
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.FAILED
    assert transaction.flwref == flwref
    assert transaction.amount == 5000
    assert transaction.rave_fee == 162.5
    assert transaction.txref == "1545676648027"
    assert transaction.id == 369835


def test_transaction_charge_with_invalid_type():
    with pytest.raises(InvalidChargeTypeError):
        Transaction.charge("invalid")   


def test_transaction_charge_type():
    Transaction.charge(CHARGE.CARD)
    Transaction.charge(CHARGE.BANK)
    Transaction.charge("card")
    Transaction.charge("bank")


def test_transaction_charge_has_initiate():
    charge = Transaction.charge(CHARGE.CARD)
    assert hasattr(charge, 'initiate')
    assert callable(charge.initiate)

def test_initiate_transaction_card_charge(api):
    data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "pin": "3310",
        "amount": "4500",
        "email": "jbravo@gmail.com",
        "suggested_auth": SUGGESTED_AUTH.PIN.value,
        "phone_number": "08012345678",
        "first_name": "Johnny",
        "last_name": "Bravo",
        "txref": "titccwpa005",
        "metadata": [
            {"metaname": "from", "metavalue":"titcc"}
        ]
    }
    response = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert isinstance(response, Transaction)
    assert response.txref == "titccwpa005"
    

def test_validate_transaction_card_charge(api):
    flwref = "FLW-MOCK-95b6e9e5d191968c19b67d2aef3cbc60"
    transaction = Transaction()
    transaction.flwref = flwref
    response = transaction.validate("12345")
    assert isinstance(response, Response)

