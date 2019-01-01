import requests
import json
from .api import default_api
from .response import Response
from .enums import TRANSACTION_STATUS, RESPONSE_STATUS, CHARGE, SUGGESTED_AUTH
from .parameters import *
from .util import validate_params, encrypt_data
from .exceptions import TrasactionNotFoundError, InvalidChargeTypeError, RaveError


class Transaction:

    def __init__(self):
        self.id = None
        self.txref = None
        self.flwref = None
        self.device_fingerprint = None
        self.amount = None
        self.currency = None
        self.rave_fee = None
        self.merchant_fee = None
        self.charged_amount = None
        self.charge_code = None
        self.charge_message = None
        self.auth_model = None
        self.auth_url = None
        self.ip = None
        self.status = None
        self.payment_type = None
        self.date_created = None
        self.metadata = None
        self.raw_data = None


    def validate(self, otp, api=None):
        api = api or default_api()
        root = api.root_url
        card_url = root+"/flwv3-pug/getpaidx/api/validatecharge"
        account_url = root+"/flwv3-pug/getpaidx/api/validate"
        card_key = "transaction_reference"
        acct_key = "transactionreference"
        url = account_url if self.payment_type == "account" else card_url
        txref_key = acct_key if self.payment_type == "account" else card_key
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        post_data = {
            "PBFPubKey":api.public_key,
            txref_key: self.flwref,
            "otp":otp
        }
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        response =  Response.from_dict(response.json())
        return response
    

    @classmethod
    def verify(cls, txref, flwref=None, api=None):
        api = api or default_api()
        root = api.root_url
        root = api.root_url
        url = root+"/flwv3-pug/getpaidx/api/v2/verify"
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        post_data = {
            "SECKEY": api.private_key,
            'txref': txref,
            'flwref': flwref
        }
        post_data = {k:v for k,v in post_data.items() if bool(v)}
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        res = Response.from_dict(response.json())
        if res.status == RESPONSE_STATUS.SUCCESS:
            if res.data['status'] == "successful" and res.data['chargecode'] == "00":
                return TRANSACTION_STATUS.SUCCESS
            return TRANSACTION_STATUS(res.data['status'])
        else:
            raise TrasactionNotFoundError("Transaction not found")


    @classmethod
    def get(cls, txref, flwref=None, api=None):
        api = api or default_api()
        root = api.root_url
        url = root+"/flwv3-pug/getpaidx/api/v2/verify"
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        post_data = {
            "SECKEY": api.private_key,
            'txref': txref,
            'flwref': flwref
        }
        post_data = {k:v for k,v in post_data.items() if bool(v)}
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        res = Response.from_dict(response.json())
        if res.status == RESPONSE_STATUS.SUCCESS and res.data:
            return cls.__from_dict(res.data)
            


    @classmethod
    def list(cls, data=None, api=None, **kwargs):
        api = api or default_api()
        data = validate_params(data or kwargs, TRANSACTION_LIST_PARAMETER_GUIDE)
        data['seckey'] = api.private_key
        root = api.root_url
        url = root+"/v2/gpx/transactions/query"
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        res = Response.from_dict(response.json())
        return res


    @classmethod
    def charge(cls, charge_type):

        __charge_type_guide_mapping = {
            CHARGE.CARD: CARD_CHARGE_PARAMETER_GUIDE,
            CHARGE.CARD.value: CARD_CHARGE_PARAMETER_GUIDE,
            CHARGE.ACCOUNT: ACCOUNT_CHARGE_PARAMETER_GUIDE,
            CHARGE.ACCOUNT.value: ACCOUNT_CHARGE_PARAMETER_GUIDE
        }

        try:
            guide = __charge_type_guide_mapping[charge_type]
        except KeyError:
            raise InvalidChargeTypeError("Charge type is not supported")

        def __initiate(data=None, api=None, **kwargs):
            api = api or default_api()
            data = validate_params(data or kwargs, guide)
            data["PBFPubKey"] = api.public_key
            if charge_type == CHARGE.ACCOUNT:
                data["payment_type"] = "account"
            root = api.root_url
            url = root+"/flwv3-pug/getpaidx/api/charge"
            headers = {
                'content-type': 'application/json',
                'accept': 'application/json'
            }
            encrypted_data = encrypt_data(json.dumps(data), api.private_key)
            post_data = {
                "PBFPubKey":api.public_key,
                "client": encrypted_data,
                "alg":"3DES-24"
            }
            response = requests.post(url, data=json.dumps(post_data), headers=headers)
            response = Response.from_dict(response.json())
            # TODO: remove debug print statements
            print("\n\n\n")
            print("from initiate charge")
            print(response.status)
            print(response.message)
            print(response.data)
            print("\n\n\n")
            if response.status == RESPONSE_STATUS.SUCCESS:
                if "suggested_auth" in response.data:
                    return SUGGESTED_AUTH(response.data.get("suggested_auth"))
                else:
                    return cls.__from_dict(response.data)
            else:
                if 'tx' in response.data:
                    return cls.__from_dict(response.data.get('tx'))
                else:
                    raise RaveError(response.message)
                    
        return type("__Charge", (), {'initiate':__initiate})


    @classmethod
    def __from_dict(cls, data):
        transaction = cls()
        transaction.id = data.get('txid') or data.get('id')
        transaction.txref = data.get('txref') or data.get('txRef')
        transaction.flwref = data.get('flwref') or data.get('flwRef')
        transaction.device_fingerprint = data.get("devicefingerprint") or data.get('device_fingerprint')
        transaction.amount = data.get("amount")
        transaction.currency = data.get("currency")
        transaction.charge_code = data.get("chargecode") or data.get('chargeResponseCode')
        transaction.charge_message = data.get("chargemessage") or data.get('chargeResponseMessage')
        transaction.charged_amount = data.get("chargedamount") or data.get('charged_amount')
        transaction.rave_fee = data.get("appfee")
        transaction.merchant_fee = data.get("merchantfee")
        transaction.auth_model = data.get("authmodel") or data.get("authModelUsed")
        transaction.auth_url = data.get("authurl")
        transaction.ip = data.get("ip") or data.get("IP")
        transaction.status = TRANSACTION_STATUS(data.get('status'))
        transaction.payment_type = data.get("paymenttype") or data.get("paymentType")
        transaction.date_created = data.get("created") or data.get("createdAt")
        transaction.date_updated = data.get("updatedAt")
        transaction.metadata = data.get("meta")
        transaction.raw_data = data
        return transaction

    
    