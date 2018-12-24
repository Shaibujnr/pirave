import time


CARD_CHARGE_PARAMETERS = [
    # ('flutterwave_param', 'function_argument', required, default)
    ("cardno", "cardno", True, None),
    ("cvv", "cvv", True, None),
    ("expirymonth", "expiry_month", True, None),
    ("expiryyear", "expiry_year", True, None),
    ("currency", "currency", False, "NGN"),
    ("country", "country", False, "NG"),
    ("pin", "pin", False, None),
    ("suggested_auth", "suggested_auth", False, "PIN"),
    ("amount", "amount", True, None),
    ("email", "email", True, None),
    ("phonenumber", "phone_number", True, None),
    ("firstname", "first_name", True, None),
    ("lastname", "last_name", True, None),
    ("IP", "ip", False, None),
    ("txRef", "txref", True, str(int(round(time.time() * 1000)))),
    ("device_fingerprint", "device_fingerprint", False, None),
    ("charge_type", "charge_type", False, None),
    ("subaccounts", "sub_accounts", False, None),
    ("meta", "metadata", False, None),
    ("redirect_url", "redirect_url", False, None),
]