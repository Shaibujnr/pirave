import pytest
from pirave.enums import (CHARGE, RESPONSE_STATUS, SUGGESTED_AUTH,
                          TRANSACTION_STATUS)
from pirave.response import Response
from pirave.transaction import Transaction
from pirave.util import get_time_ms
from pirave.exceptions import RaveError


def test_pay_with_access_bank_account(api):
    data = {
        "account_number": "0690000031",
        "bank": "044",
        "amount": 100,
        "email": "test_pay_with_account@gmail.com",
        "phone_number": "08012345678",
        "first_name": "Transaction",
        "last_name": "Bank",
        "txref": "msa-%s"%get_time_ms(),
        "bvn": "nobvn",
        "pass_code": "nopasscode",
        "metadata":[
            {"metaname": "from"},
            {"metavalue": "function::test_pay_with_account"}
        ]
    }
    transaction = Transaction.charge(CHARGE.ACCOUNT).initiate(**data)
    assert isinstance(transaction, Transaction)
    assert transaction.payment_type == "account"
    assert transaction.flwref is not None
    assert transaction.charge_code == "02"
    assert transaction.status == TRANSACTION_STATUS.PENDING
    assert transaction.raw_data is not None
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS


def test_pay_with_providus_bank_account(api):
    data = {
        "account_number": "5900102340",
        "bank": "101",
        "amount": 100,
        "email": "test_pay_with_account@gmail.com",
        "phone_number": "08012345678",
        "first_name": "Transaction",
        "last_name": "Bank",
        "txref": "msa-%s"%get_time_ms(),
        "bvn": "nobvn",
        "pass_code": "nopasscode",
        "metadata":[
            {"metaname": "from"},
            {"metavalue": "function::test_pay_with_account"}
        ]
    }
    transaction = Transaction.charge(CHARGE.ACCOUNT).initiate(**data)
    assert isinstance(transaction, Transaction)
    assert transaction.payment_type == "account"
    assert transaction.flwref is not None
    assert transaction.charge_code == "00"
    assert transaction.status == TRANSACTION_STATUS.SUCCESS
    assert transaction.raw_data is not None
    

def test_pay_with_providus_bank_account_again(api):
    data = {
        "account_number": "5900002567",
        "bank": "101",
        "amount": 100,
        "email": "test_pay_with_account@gmail.com",
        "phone_number": "08012345678",
        "first_name": "Transaction",
        "last_name": "Bank",
        "txref": "msa-%s"%get_time_ms(),
        "bvn": "nobvn",
        "pass_code": "nopasscode",
        "metadata":[
            {"metaname": "from"},
            {"metavalue": "function::test_pay_with_account"}
        ]
    }
    transaction = Transaction.charge(CHARGE.ACCOUNT).initiate(**data)
    assert isinstance(transaction, Transaction)
    assert transaction.payment_type == "account"
    assert transaction.flwref is not None
    assert transaction.charge_code == "00"
    assert transaction.status == TRANSACTION_STATUS.SUCCESS
    assert transaction.raw_data is not None