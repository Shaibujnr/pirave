import pytest
from pirave.response import Response
from pirave.enums import RAVERESPONSE
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
    assert response.status == RAVERESPONSE.SUCCESS


def test_initialize_card_charge_with_pin_auth(api):
    response = CardCharge.initiate({
        "cardno": "5438898014560229",
        "cvv": "789",
        "expiry_month": "09",
        "expiry_year": "19",
        "pin": "3310",
        "amount": "100",
        "email": "jane@gmail.com",
        "suggested_auth": "PIN",
        "phone_number": "08012345678",
        "first_name": "Jane",
        "last_name": "Doe",
        "txref": "712480329"
    })
    print(response.data)
    assert response.status == RAVERESPONSE.SUCCESS
    