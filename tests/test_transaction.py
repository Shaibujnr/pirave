import pytest
from pirave.response import Response
from pirave.enums import RESPONSE_STATUS, TRANSACTION_STATUS
from pirave.transaction import Transaction
from pirave.exceptions import TrasactionNotFoundError


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
