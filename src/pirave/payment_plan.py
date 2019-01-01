import requests
import json
from .api import default_api
from .response import Response
from .enums import RESPONSE_STATUS, PAYMENT_PLAN_STATUS
from .exceptions import RaveError


class PaymentPlan:
    def __init__(self):
        self.id = None
        self.name = None
        self.amount = None
        self.interval = None
        self.duration = None
        self.status = None
        self.currency = None
        self.token = None
        self.date_created = None


    def cancel(self, api=None):
        api = api or default_api()
        path = "/v2/gpx/paymentplans/%s/cancel"%str(self.id)
        url = api.root_url+path
        post_data = {"seckey":api.private_key}
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        res = Response.from_dict(response.json())
        # TODO: remove debug print statements
        print("\n\n\n")
        print("from cancel payment plan")
        print(res.status)
        print(res.message)
        print(res.data)
        print("\n\n\n")
        if res.status  == RESPONSE_STATUS.SUCCESS:
            data = res.data
            self.id = data['id']
            self.name = data['name']
            self.amount = float(data['amount'])
            self.interval = data['interval']
            self.duration = int(data['duration'])
            self.status = PAYMENT_PLAN_STATUS(data['status'])
            self.currency = data['currency']
            self.token = data['uuid']
            self.date_created = data['createdAt']
        else:
            raise RaveError(res.message)


    def update(self, name, status, api=None):
        api = api or default_api()
        path = "/v2/gpx/paymentplans/%s/edit"%str(self.id)
        url = api.root_url+path
        status = status.value if isinstance(status, PAYMENT_PLAN_STATUS) else status
        post_data = {"seckey":api.private_key, "name":name, "status":status}
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        res = Response.from_dict(response.json())
        # TODO: remove debug print statements
        print("\n\n\n")
        print("from update payment plan")
        print(res.status)
        print(res.message)
        print(res.data)
        print("\n\n\n")
        if res.status  == RESPONSE_STATUS.SUCCESS:
            data = res.data
            self.id = data['id']
            self.name = data['name']
            self.amount = float(data['amount'])
            self.interval = data['interval']
            self.duration = int(data['duration'])
            self.status = PAYMENT_PLAN_STATUS(data['status'])
            self.currency = data['currency']
            self.token = data['uuid']
            self.date_created = data['createdAt']
        else:
            raise RaveError(res.message)


    @classmethod
    def create(cls, name, interval, amount=None, duration=None, api=None):
        api = api or default_api()
        path = "/v2/gpx/paymentplans/create"
        url = api.root_url+path
        post_data = {
            "amount": amount,
            "name": name,
            "interval": interval,
            "duration": duration,
            "seckey": api.private_key
        }
        post_data = {k:v for k,v in post_data.items() if bool(v)}
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        res = Response.from_dict(response.json())
        # TODO: remove print debug print statements
        print("\n\n\n")
        print("from crate payment plan")
        print(res.status)
        print(res.message)
        print(res.data)
        print("\n\n\n")
        if res.status == RESPONSE_STATUS.SUCCESS:
            payment_plan = PaymentPlan()
            payment_plan.id = res.data['id']
            payment_plan.name = res.data['name']
            payment_plan.amount = float(res.data['amount'])
            payment_plan.interval = res.data['interval']
            payment_plan.duration = int(res.data['duration'])
            payment_plan.status = PAYMENT_PLAN_STATUS(res.data['status'])
            payment_plan.currency = res.data['currency']
            payment_plan.token = res.data['plan_token']
            payment_plan.date_created = res.data['date_created']
            return payment_plan
        else:
            raise RaveError(res.message)


    @classmethod    
    def list(cls, api=None):
        plans = []
        api = api or default_api()
        path = "/v2/gpx/paymentplans/query"
        url = api.root_url+path
        params = {"seckey": api.private_key}
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        response = requests.get(url, params=params, headers=headers)
        res = Response.from_dict(response.json())
        # TODO: remove debug print statements
        print("\n\n\n")
        print("from list payment plans")
        print(res.status)
        print(res.message)
        print(res.data)
        print("\n\n\n")
        if res.status  == RESPONSE_STATUS.SUCCESS:
            data_list = res.data['paymentplans']
            for data in data_list:
                payment_plan = PaymentPlan()
                payment_plan.id = data['id']
                payment_plan.name = data['name']
                payment_plan.amount = float(data['amount'])
                payment_plan.interval = data['interval']
                payment_plan.duration = int(data['duration'])
                payment_plan.status = PAYMENT_PLAN_STATUS(data['status'])
                payment_plan.currency = data['currency']
                payment_plan.token = data['plan_token']
                payment_plan.date_created = data['date_created']
                plans.append(payment_plan)
        else:
            raise RaveError(res.message)
        return plans
        


    @classmethod    
    def get(cls, id, name=None, api=None):
        api = api or default_api()
        path = "/v2/gpx/paymentplans/query"
        url = api.root_url+path
        params = {"seckey":api.private_key, "id":id, "q":name}
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        response = requests.get(url, params=params, headers=headers)
        res = Response.from_dict(response.json())
        # TODO: remove debug print statements
        print("\n\n\n")
        print("from get payment plan")
        print(res.status)
        print(res.message)
        print(res.data)
        print("\n\n\n")
        if res.status  == RESPONSE_STATUS.SUCCESS:
            data = res.data['paymentplans'][0]
            payment_plan = PaymentPlan()
            payment_plan.id = data['id']
            payment_plan.name = data['name']
            payment_plan.amount = float(data['amount'])
            payment_plan.interval = data['interval']
            payment_plan.duration = int(data['duration'])
            payment_plan.status = PAYMENT_PLAN_STATUS(data['status'])
            payment_plan.currency = data['currency']
            payment_plan.token = data['plan_token']
            payment_plan.date_created = data['date_created']
            return payment_plan
        else:
            raise RaveError(res.message)
        