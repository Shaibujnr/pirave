import requests
import json
from .api import default_api
from .response import Response
from .enums import TRANSACTION_STATUS, RESPONSE_STATUS
from .parameters import TRANSACTION_LIST_PARAMETER_GUIDE
from .util import validate_params
from .exceptions import TrasactionNotFoundError


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
        self.auth_model = None
        self.ip = None
        self.status = None
        self.payment_type = None
        self.date_created = None
        self.metadata = None
        self.raw_data = None
    

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
            transaction = Transaction()
            transaction.id = res.data['txid']
            transaction.txref = res.data['txref']
            transaction.flwref = res.data['flwref']
            transaction.device_fingerprint = res.data["devicefingerprint"]
            transaction.amount = res.data["amount"]
            transaction.currency = res.data["currency"]
            transaction.charged_amount = res.data["chargedamount"]
            transaction.rave_fee = res.data["appfee"]
            transaction.merchant_fee = res.data["merchantfee"]
            transaction.auth_model = res.data["authmodel"]
            transaction.ip = res.data["ip"]
            transaction.status = TRANSACTION_STATUS(res.data['status'])
            transaction.payment_type = res.data["paymenttype"]
            transaction.date_created = res.data["created"]
            transaction.metadata = res.data["meta"]
            transaction.raw_data = res.data
            return transaction


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
