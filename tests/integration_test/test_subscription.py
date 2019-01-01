from pirave.enums import (CHARGE, RESPONSE_STATUS, SUGGESTED_AUTH,
                          TRANSACTION_STATUS, PAYMENT_PLAN_STATUS)
from pirave.response import Response
from pirave.transaction import Transaction
from pirave.payment_plan import PaymentPlan
from pirave.util import get_time_ms


def test_card_subscription_with_plan_of_no_amount(api):
    """
    test subscribing to a plan that was created with no intial
    amount passed during plan creation.
    """
    # create a payment plan with no amount
    plan = PaymentPlan.create("No Amount Plan", "daily", None, None)
    assert isinstance(plan, PaymentPlan)
    assert plan.id is not None
    charge_data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "pin": "3310",
        "amount": "49450.02",
        "email": "test_card_subscription_with_plan_of_no_amount@gmail.com",
        "suggested_auth": SUGGESTED_AUTH.PIN.value,
        "phone_number": "08012345678",
        "first_name": "Chin",
        "last_name": "Xiao",
        "txref": "tcswpna-%s"%get_time_ms(),
        "payment_plan": plan.id,
        "metadata": [
            {"metaname": "from", "metavalue":"tcswpna"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**charge_data)
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS


def test_card_sbscription_to_already_subscribed_plan_of_no_amount(api):
    """
    test subscribing to a plan that was created with no intial
    amount passed during plan creation but has previously been subscribed to
    by a customer
    """
    plan_id = 1340
    charge_data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "pin": "3310",
        "amount": "2300.45", #different from the initially subscribed amount
        "email": "test_card_sbscription_to_already_subscribed_plan_of_no_amount@gmail.com",
        "suggested_auth": SUGGESTED_AUTH.PIN.value,
        "phone_number": "08012345678",
        "first_name": "Chin",
        "last_name": "Xiao",
        "txref": "tcstaspona-%s"%get_time_ms(),
        "payment_plan": plan_id,
        "metadata": [
            {"metaname": "from", "metavalue":"tcstaspona"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**charge_data)
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS


def test_card_sbscription_with_different_amount(api):
    """
    test subscribing to a plan by charging different amount from the amount
    the plan was created with
    """
    plan = PaymentPlan.create("Different Amount Plan", "daily", 6789, None)
    assert isinstance(plan, PaymentPlan)
    assert plan.id is not None
    charge_data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "pin": "3310",
        "amount": "8740.33", #different from the created plan amount
        "email": "test_card_sbscription_with_different_amount@gmail.com",
        "suggested_auth": SUGGESTED_AUTH.PIN.value,
        "phone_number": "08012345678",
        "first_name": "Chin",
        "last_name": "Xiao",
        "txref": "tcswda-%s"%get_time_ms(),
        "payment_plan": plan.id,
        "metadata": [
            {"metaname": "from", "metavalue":"tcswda"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**charge_data)
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS


def test_card_sbscription_to_cancelled_plan(api):
    """
    test subscribing to a plan which has been cancelled
    """
    plan = PaymentPlan.create("Cancelled Plan", "daily", 3200, None)
    assert isinstance(plan, PaymentPlan)
    assert plan.id is not None
    plan.cancel()
    assert plan.status == PAYMENT_PLAN_STATUS.CANCELLED
    charge_data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "pin": "3310",
        "amount": "8000", 
        "email": "test_card_sbscription_to_cancelled_plan@gmail.com",
        "suggested_auth": SUGGESTED_AUTH.PIN.value,
        "phone_number": "08012345678",
        "first_name": "Chin",
        "last_name": "Xiao",
        "txref": "tcstcp-%s"%get_time_ms(),
        "payment_plan": plan.id,
        "metadata": [
            {"metaname": "from", "metavalue":"tcstcp"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**charge_data)
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS


def test_card_sbscription_to_plan_with_duration(api):
    """
    test subscribing to a plan which has a duration
    """
    plan = PaymentPlan.create("Duration Plan", "daily", 5000, 3)
    assert isinstance(plan, PaymentPlan)
    assert plan.id is not None
    charge_data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "pin": "3310",
        "amount": "8000", 
        "email": "test_card_sbscription_with_duration@gmail.com",
        "suggested_auth": SUGGESTED_AUTH.PIN.value,
        "phone_number": "08012345678",
        "first_name": "Chin",
        "last_name": "Xiao",
        "txref": "tcstpwd-%s"%get_time_ms(),
        "payment_plan": plan.id,
        "metadata": [
            {"metaname": "from", "metavalue":"tcstpwd"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**charge_data)
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS
