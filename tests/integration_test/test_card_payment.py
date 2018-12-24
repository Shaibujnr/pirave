from pirave.charge import CardCharge
from pirave.response import Response
from pirave.util import get_time_ms
from pirave.enums import SUGGESTED_AUTH, RESPONSE_STATUS


def test_card_declined(api):
    response = CardCharge.initiate({
        "cardno": "5143010522339965",
        "cvv": " 276",
        "expiry_month": "08",
        "expiry_year": "19",
        # "pin": "3310",
        "amount": "5000",
        "email": "john_card_declined@gmail.com",
        # "suggested_auth": "PIN",
        "phone_number": "08099899897",
        "first_name": "John",
        "last_name": "Doe",
        "txref": get_time_ms(),
        "suggested_auth": SUGGESTED_AUTH.NOAUTH_INTERNATIONAL.value,
        "billing_zip": "07205",
        "billing_city": "Hillside",
        "billing_address": "470 Mundet PI",
        "billing_state": "NJ",
        "billing_country": "US",
    })
    print("\n\n\n")
    print("From test card payment")
    print(response.status)
    print(response.message)
    print(response.data)
    print("\n\n\n")
    assert response.status == RESPONSE_STATUS.ERROR