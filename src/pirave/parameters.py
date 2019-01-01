CARD_CHARGE_PARAMETER_GUIDE = [
    # ('flutterwave_param', 'function_argument', required, default)
    ("cardno", "cardno", True, None),
    ("cvv", "cvv", True, None),
    ("expirymonth", "expiry_month", True, None),
    ("expiryyear", "expiry_year", True, None),
    ("currency", "currency", False, "NGN"),
    ("country", "country", False, "NG"),
    ("pin", "pin", False, None),
    ("suggested_auth", "suggested_auth", False, None),
    ("amount", "amount", True, None),
    ("email", "email", True, None),
    ("phonenumber", "phone_number", True, None),
    ("firstname", "first_name", True, None),
    ("lastname", "last_name", True, None),
    ("IP", "ip", False, None),
    ("txRef", "txref", True, None),
    ("device_fingerprint", "device_fingerprint", False, None),
    ("charge_type", "charge_type", False, None),
    ("subaccounts", "sub_accounts", False, None),
    ("meta", "metadata", False, None),
    ("redirect_url", "redirect_url", False, None),
    ("billingzip", "billing_zip", False, None),
    ("billingcity", "billing_city", False, None),
    ("billingaddress", "billing_address", False, None),
    ("billingstate", "billing_state", False, None),
    ("billingcountry", "billing_country", False, None),
    ("payment_plan", "payment_plan", False, None),
]

ACCOUNT_CHARGE_PARAMETER_GUIDE = [
    ("accountnumber", "account_number", True, None),
    ("accountbank", "bank", True, None),
    ("currency", "currency", False, "NGN"),
    ("country", "country", False, "NG"),
    ("amount", "amount", True, None),
    ("email", "email", True, None),
    ("phonenumber", "phone_number", True, None),
    ("firstname", "first_name", True, None),
    ("lastname", "last_name", True, None),
    ("IP", "ip", False, None),
    ("txRef", "txref", True, None),
    ("bvn", "bvn", True, None), #Required for UBA bank accounts
    ("passcode", "pass_code", True, None), #Required for Zenith bank accounts
    ("device_fingerprint", "device_fingerprint", False, None),
    ("redirect_url", "redirect_url", False, None),
    ("subaccounts", "sub_accounts", False, None),
    ("meta", "metadata", False, None),
]

TRANSACTION_LIST_PARAMETER_GUIDE = [
    ('from', 'start_date', False, None),
    ('to', "end_date", False, None),
    ('page', 'page', False, None),
    ('customer_email', 'customer_email', False, None),
    ('status', 'status', False, None),
    ('customer_fullname', 'customer_fullname', False, None),
    ('transaction_reference', 'txref', False, None),
    ('currency', 'currency', False, None)
]