import pytest
from pirave.response import Response
from pirave.enums import RESPONSE_STATUS, TRANSACTION_STATUS, CHARGE, SUGGESTED_AUTH
from pirave.transaction import Transaction
from pirave.exceptions import TrasactionNotFoundError, InvalidChargeTypeError, RaveError


def test_verify_transaction_with_txref(api):
    txref = "712480329"
    response = Transaction.verify(txref)
    assert response == TRANSACTION_STATUS.PENDING


def test_verify_transaction_with_flwref(api):
    flwref = "FLW-MOCK-bda70b433a1fdb577dbb880ae1ee37b2"
    response = Transaction.verify(None, flwref)
    assert response == TRANSACTION_STATUS.SUCCESS


def test_verify_transaction_with_unrelated_flwref_and_txref(api):
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
    Transaction.charge(CHARGE.ACCOUNT)
    Transaction.charge("card")
    Transaction.charge("account")


def test_charge_has_initiate():
    charge = Transaction.charge(CHARGE.CARD)
    assert hasattr(charge, 'initiate')
    assert callable(charge.initiate)


def test_initiate_card_charge(api):
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
    

def test_initiate_bank_charge(api):
    data = {
        "account_number": "0690000031",
        "bank": "044",
        "amount": 100,
        "email": "tbank@gmail.com",
        "phone_number": "08012345678",
        "first_name": "Transaction",
        "last_name": "Bank",
        "txref": "bbankref",
        "bvn": "nobvn",
        "pass_code": "nopasscode",
        "metadata":[
            {"metaname": "test_pirave"},
            {"metavalue": "function::test_initiate_transaction_bank_charge"}
        ]
    }
    response = Transaction.charge(CHARGE.ACCOUNT).initiate(**data)
    assert isinstance(response, Transaction)
    assert response.txref == "bbankref"
    assert response.payment_type == "account"
    assert response.flwref is not None
    assert response.charge_code == "02"
    assert response.status == TRANSACTION_STATUS.PENDING
    assert response.raw_data is not None


def test_initiate_card_charge_with_wrong_cardno(api):
    data = {
        "cardno": "000000000000",
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
    with pytest.raises(RaveError):
        Transaction.charge(CHARGE.CARD).initiate(**data)


def test_initiate_card_charge_with_expired_card(api):
    data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "01",
        "expiry_year": "17",
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
    with pytest.raises(RaveError):
        Transaction.charge(CHARGE.CARD).initiate(**data)


def test_initiate_card_charge_with_wrong_pin(api):
    data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "04",
        "expiry_year": "89",
        "pin": "9034543",
        "amount": 4500,
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
    with pytest.raises(RaveError):
        Transaction.charge(CHARGE.CARD).initiate(**data)


def test_initiate_card_charge_with_negative_amount(api):
    data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "04",
        "expiry_year": "89",
        "pin": "3310",
        "amount": -4500,
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
    with pytest.raises(RaveError):
        Transaction.charge(CHARGE.CARD).initiate(**data)


def test_initiate_bank_charge_with_wrong_account_number(api):
    data = {
        # "account_number": "0690000031",
        "account_number": "0000000000",
        "bank": "044",
        "amount": 100,
        "email": "tbank@gmail.com",
        "phone_number": "08012345678",
        "first_name": "Transaction",
        "last_name": "Bank",
        "txref": "bbankref",
        "bvn": "nobvn",
        "pass_code": "nopasscode",
        "metadata":[
            {"metaname": "test_pirave"},
            {"metavalue": "function::test_initiate_transaction_bank_charge"}
        ]
    }
    with pytest.raises(RaveError):
        Transaction.charge(CHARGE.ACCOUNT).initiate(**data)


def test_initiate_bank_charge_with_wrong_bank_code(api):
    data = {
        "account_number": "0690000031",
        "bank": "000",
        "amount": 100,
        "email": "tbank@gmail.com",
        "phone_number": "08012345678",
        "first_name": "Transaction",
        "last_name": "Bank",
        "txref": "bbankref",
        "bvn": "nobvn",
        "pass_code": "nopasscode",
        "metadata":[
            {"metaname": "test_pirave"},
            {"metavalue": "function::test_initiate_transaction_bank_charge"}
        ]
    }
    with pytest.raises(RaveError):
        Transaction.charge(CHARGE.ACCOUNT).initiate(**data)
