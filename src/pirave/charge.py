import requests
import json
from .parameters import CARD_CHARGE_PARAMETER_GUIDE
from .util import encrypt_data, validate_params
from .api import default_api, Api
from .response import Response


class CardCharge:
    
    @classmethod
    def initiate(cls, data=None, api=None, **kwargs):
        api = api or default_api()
        data = validate_params(data or kwargs, CARD_CHARGE_PARAMETER_GUIDE)
        data["PBFPubKey"] = api.public_key
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
        return Response.from_dict(response.json())


    @classmethod
    def validate(cls, flw_reference, otp, api=None):
        api = api or default_api()
        root = api.root_url
        url = root+"/flwv3-pug/getpaidx/api/validatecharge"
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        post_data = {
            "PBFPubKey":api.public_key,
            "transaction_reference": flw_reference,
            "otp":otp
        }
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        return Response.from_dict(response.json())
