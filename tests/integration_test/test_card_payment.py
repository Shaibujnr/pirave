from pirave.enums import (CHARGE, RESPONSE_STATUS, SUGGESTED_AUTH,
                          TRANSACTION_STATUS)
from pirave.response import Response
from pirave.transaction import Transaction
from pirave.util import get_time_ms


def test_pay_with_master_card_pin_auth(api):
    pin = "3310"
    data = {
        "cardno": "5399838383838381",
        "cvv": "470",
        "expiry_month": "10",
        "expiry_year": "22",
        "amount": "8400.50",
        "email": "test_pay_with_master_card_pin_auth@gmail.com",
        "phone_number": "08012345678",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwmcpa-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwmcpa"}
        ]
    }
    suggested_auth = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert suggested_auth == SUGGESTED_AUTH.PIN
    data["pin"] = pin
    data["suggested_auth"] = SUGGESTED_AUTH.PIN.value
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS
    

def test_pay_with_card_declined(api):
    data = {
        "cardno": "5143010522339965",
        "cvv": "276",
        "expiry_month": "08",
        "expiry_year": "19",
        "amount": 6700.54,
        "email": "test_pay_with_card_declined@gmail.com",
        "phone_number": "08012345678",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwcd-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwcd"}
        ]
    }
    suggested_auth = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert suggested_auth == SUGGESTED_AUTH.NOAUTH_INTERNATIONAL
    data["billing_zip"] = "07205"
    data["billing_city"] = "Hillside"
    data["billing_address"] = "470 Mundet PI"
    data["billing_state"] = "NJ"
    data["billing_country"] = "US"
    data["suggested_auth"] = SUGGESTED_AUTH.NOAUTH_INTERNATIONAL.value
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    print(transaction.auth_url)
    assert transaction.status == TRANSACTION_STATUS.FAILED
    

def test_pay_with_card_fraudulent(api):
    data = {
        "cardno": "5590131743294314",
        "cvv": "887",
        "expiry_month": "11",
        "expiry_year": "20",
        "amount": 90865,
        "email": "test_pay_with_card_fraudulent@gmail.com",
        "phone_number": "08012345678",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwcf-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwcf"}
        ]
    }
    suggested_auth = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert suggested_auth == SUGGESTED_AUTH.NOAUTH_INTERNATIONAL
    data["billing_zip"] = "07205"
    data["billing_city"] = "Hillside"
    data["billing_address"] = "470 Mundet PI"
    data["billing_state"] = "NJ"
    data["billing_country"] = "US"
    data["suggested_auth"] = SUGGESTED_AUTH.NOAUTH_INTERNATIONAL.value
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    print(transaction.auth_url)
    assert transaction.status == TRANSACTION_STATUS.FAILED


def test_pay_with_card_insufficient_fund(api):
    data = {
        "cardno": "5258585922666506",
        "cvv": "883",
        "expiry_month": "09",
        "expiry_year": "19",
        "amount": "8400.50",
        "email": "test_pay_with_master_card_pin_auth@gmail.com",
        "phone_number": "08012345678",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwmcpa-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwmcpa"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    assert transaction.status == TRANSACTION_STATUS.FAILED
    


def test_pay_with_master_card_3ds_auth(api):
    pin = "3310"
    data = {
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "amount": "8400.50",
        "email": "test_pay_with_master_card_3ds_auth@gmail.com",
        "phone_number": "08014830945",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwmc3ds-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwmc3ds"}
        ]
    }
    suggested_auth = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert suggested_auth == SUGGESTED_AUTH.PIN
    data["pin"] = pin
    data["suggested_auth"] = SUGGESTED_AUTH.PIN.value
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS


def test_pay_with_visa_card_no_auth(api):
    data = {
        "cardno": "4751763236699647",
        "cvv": "800",
        "expiry_month": "09",
        "expiry_year": "21",
        "amount": 45500,
        "email": "test_pay_with_visa_card_no_auth@gmail.com",
        "phone_number": "08078653450",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwvcna-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwvcna"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.SUCCESS


def test_pay_with_visa_card_no_auth_again(api):
    data = {
        "cardno": "4242424242424242",
        "cvv": "812",
        "expiry_month": "01",
        "expiry_year": "19",
        "amount": 45500,
        "email": "test_pay_with_visa_card_no_auth@gmail.com",
        "phone_number": "08078653450",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwvcna-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwvcna"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    assert isinstance(transaction, Transaction)
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response is not None
    assert isinstance(response, Response)
    assert response.status == RESPONSE_STATUS.SUCCESS


def test_pay_with_verve_card(api):
    pin = "3310"
    data = {
        "cardno": "5061460410120223210",
        "cvv": "780",
        "expiry_month": "12",
        "expiry_year": "21",
        "amount": "8400.50",
        "email": "test_pay_with_verve_card@gmail.com",
        "phone_number": "08012345678",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwvc-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwvc"}
        ]
    }
    suggested_auth = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert suggested_auth == SUGGESTED_AUTH.PIN
    data["pin"] = pin
    data["suggested_auth"] = SUGGESTED_AUTH.PIN.value
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    assert transaction.status == TRANSACTION_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS


def test_pay_with_visa_card_local(api):
    data = {
        "cardno": "4187427415564246",
        "cvv": "828",
        "expiry_month": "09",
        "expiry_year": "19",
        "amount": 23456.50,
        "email": "test_pay_with_visa_card_local@gmail.com",
        "phone_number": "08012345678",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwvcl-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwvcl"}
        ]
    }
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    assert transaction.status == TRANSACTION_STATUS.PENDING
    response = transaction.validate("12345")
    assert response.status == RESPONSE_STATUS.SUCCESS
    status = Transaction.verify(transaction.txref)
    assert status == TRANSACTION_STATUS.SUCCESS
    

def test_pay_with_visa_card_international(api):
    data = {
        "cardno": "4556052704172643",
        "cvv": "899",
        "expiry_month": "01",
        "expiry_year": "19",
        "amount": 23456.50,
        "email": "test_pay_with_visa_card_international@gmail.com",
        "phone_number": "08012345678",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "tpwvci-%s"%get_time_ms(),
        "metadata": [
            {"metaname": "from", "metavalue":"tpwvci"}
        ]
    }
    suggested_auth = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert suggested_auth == SUGGESTED_AUTH.NOAUTH_INTERNATIONAL
    data["billing_zip"] = "07205"
    data["billing_city"] = "Hillside"
    data["billing_address"] = "470 Mundet PI"
    data["billing_state"] = "NJ"
    data["billing_country"] = "US"
    data["suggested_auth"] = SUGGESTED_AUTH.NOAUTH_INTERNATIONAL.value
    transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
    assert transaction is not None
    print(transaction.auth_url)
    assert transaction.status == TRANSACTION_STATUS.PENDING
    
    
# def test_pay_with_american_express_card(api):
#     data = {
#         "cardno": "344173993556638",
#         "cvv": "828",
#         "expiry_month": "01",
#         "expiry_year": "22",
#         "amount": 23456.50,
#         "email": "test_pay_with_american_express_card@gmail.com",
#         "phone_number": "08012345678",
#         "first_name": "John",
#         "last_name": "Doe",
#         "txref": "tpwaec-%s"%get_time_ms(),
#         "metadata": [
#             {"metaname": "from", "metavalue":"tpwaec"}
#         ]
#     }
#     suggested_auth = Transaction.charge(CHARGE.CARD).initiate(**data)
#     assert suggested_auth == SUGGESTED_AUTH.NOAUTH_INTERNATIONAL
#     data["billing_zip"] = "07205"
#     data["billing_city"] = "Hillside"
#     data["billing_address"] = "470 Mundet PI"
#     data["billing_state"] = "NJ"
#     data["billing_country"] = "US"
#     data["suggested_auth"] = SUGGESTED_AUTH.NOAUTH_INTERNATIONAL.value
#     transaction = Transaction.charge(CHARGE.CARD).initiate(**data)
#     assert transaction is not None
#     print(transaction.auth_url)
#     assert transaction.status == TRANSACTION_STATUS.PENDING
