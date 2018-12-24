import pytest
from pirave.response import Response
from pirave.enums import RESPONSE_STATUS, SUGGESTED_AUTH
from pirave.charge import CardCharge


def test_initialize_card_charge_without_auth(api):
    response = CardCharge.initiate({
            "cardno": "5438898014560229",
            "cvv": "789",
            "expiry_month": "09",
            "expiry_year": "19",
            "amount": "7865",
            "email": "jane@gmail.com",
            "phone_number": "08012345678",
            "first_name": "Jane",
            "last_name":"Doe",
            "txref": "712480329"
    })
    assert response is not None
    assert isinstance(response, Response)
    assert response.status == RESPONSE_STATUS.SUCCESS


def test_initialize_card_charge_with_pin_auth(api):
    response = CardCharge.initiate({
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
        "txref": "ticcwpa001"
    })
    assert response.status == RESPONSE_STATUS.SUCCESS
    

def test_validate_card_charge(api):
    response = CardCharge.initiate({
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "pin": "3310",
        "amount": "5000",
        "email": "john_validate_card_charge@gmail.com",
        "suggested_auth": SUGGESTED_AUTH.PIN.value,
        "phone_number": "08099899897",
        "first_name": "John",
        "last_name": "Doe",
        "txref": "41235"
    })
    if response.status == RESPONSE_STATUS.SUCCESS and response.data.get('chargeResponseCode')=='02':
        flwRef = response.data.get('flwRef')
        otp = '12345'
        res = CardCharge.validate(flwRef,otp)
        assert res.status == RESPONSE_STATUS.SUCCESS
    # FLW-MOCK-e31b30c8a1701abb22a8497bb19faf70

