import pytest
from pirave.exceptions import (
    MissingArgumentException,
    MissingConfigException,
    InvalidArgumentException
)
from pirave.util import validate_params, encrypt_data
from pirave.api import reset_api, default_api, configure
from pirave.enums import Environment
from pirave.parameters import CARD_CHARGE_PARAMETER_GUIDE
import json


def test_validate_params_with_missing_params():
    with pytest.raises(MissingArgumentException):
        validate_params(
            {
                "cardno": "7287423987dskljf",
                "cvv": "768",
                "expiry_month": "456",
                "expiry_year": "7879",
                "amount": 7865,
                "email": "jane@gmail.com",
                "phone_number": "9876865555",
                "first_name": "Jane",
                "last_name":"Doe",
            }, 
            CARD_CHARGE_PARAMETER_GUIDE)


def test_validate_params_with_invalid_params():
    with pytest.raises(InvalidArgumentException):
        validate_params(
            {
                "cardno": "7287423987dskljf",
                "cvv": "768",
                "expiry_month": "456",
                "expiry_year": "7879",
                "amount": 7865,
                "email": "jane@gmail.com",
                "phone_number": "9876865555",
                "first_name": "Jane",
                "last_name":"Doe",
                "txref": 712480329,
                "invalid": "argument"
            }, 
            CARD_CHARGE_PARAMETER_GUIDE)


def test_validate_params():
    data = validate_params(
        {
            "cardno": "7287423987dskljf",
            "cvv": "768",
            "expiry_month": "456",
            "expiry_year": "7879",
            "amount": 7865,
            "email": "jane@gmail.com",
            "phone_number": "9876865555",
            "first_name": "Jane",
            "last_name":"Doe",
            "txref": 712480329,
        
        }, 
        CARD_CHARGE_PARAMETER_GUIDE)

    assert bool(data) is True


def test_encryption(api):
    data = validate_params({
            "cardno": "7287423987dskljf",
            "cvv": "768",
            "expiry_month": "456",
            "expiry_year": "7879",
            "amount": 7865,
            "email": "jane@gmail.com",
            "phone_number": "9876865555",
            "first_name": "Jane",
            "last_name":"Doe",
            "txref": 712480329,
        
        }, CARD_CHARGE_PARAMETER_GUIDE)
    data["PBFPubKey"] = api.public_key
    plain_text = str(data)
    encrypted = encrypt_data(plain_text, api.private_key)
    assert encrypted is not None

