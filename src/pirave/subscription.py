import requests
import json
from .exceptions import RaveError
from .api import default_api
from .response import Response
from .enums import RESPONSE_STATUS, SUBSCRIPTION_STATUS


class Subscription:

    def __init__(self):
        self.id = None
        self.amount = None
        self.customer_id = None
        self.customer_email = None
        self.plan_id = None
        self.status = None
        self.date_created = None

    
    @classmethod
    def list(cls, api=None):
        result = []
        api = api or default_api()
        root = api.root_url
        path = "/v2/gpx/subscriptions/query"
        url = root+path
        params = {"seckey": api.private_key}
        headers = {
                'content-type': 'application/json',
                'accept': 'application/json'
        }
        response = requests.get(url, params=params, headers=headers)
        response = Response.from_dict(response.json())
        # TODO: remove debug print statements
        print("\n\n\n")
        print("from list subscriptions")
        print(response.status)
        print(response.message)
        print(response.data)
        print("\n\n\n")
        if response.status == RESPONSE_STATUS.SUCCESS:
            data_list = response.data['plansubscriptions']
            for data in data_list:
                subscription = Subscription()
                subscription.id = data['id']
                subscription.amount = data['amount']
                subscription.customer_id = data['customer']['id']
                subscription.customer_email = data['customer']['customer_email']
                subscription.plan_id = data['plan']
                subscription.status = SUBSCRIPTION_STATUS(data['status'])
                subscription.date_created = data['date_created']
                result.append(subscription)
        else:
            raise RaveError(response.message)
        return result


    @classmethod
    def get(cls, id, customer_email=None, api=None):
        api = api or default_api()
        root = api.root_url
        path = "/v2/gpx/subscriptions/query"
        url = root+path
        params = {"seckey": api.private_key, "id":id, "email":customer_email}
        headers = {
                'content-type': 'application/json',
                'accept': 'application/json'
        }
        response = requests.get(url, params=params, headers=headers)
        response = Response.from_dict(response.json())
        # TODO: remove debug print statements
        print("\n\n\n")
        print("from get subscription")
        print(response.status)
        print(response.message)
        print(response.data)
        print("\n\n\n")
        if response.status == RESPONSE_STATUS.SUCCESS:
            if len(response.data['plansubscriptions']) > 0:
                data = response.data['plansubscriptions'][0]
                subscription = Subscription()
                subscription.id = data['id']
                subscription.amount = data['amount']
                subscription.customer_id = data['customer']['id']
                subscription.customer_email = data['customer']['customer_email']
                subscription.plan_id = data['plan']
                subscription.status = SUBSCRIPTION_STATUS(data['status'])
                subscription.date_created = data['date_created']
                return subscription
            else:
                msg = "No subscription with id {0} and/or customer email {1}"
                raise RaveError(msg.format(id,customer_email))
        else:
            raise RaveError(response.message)


    def cancel(self, api=None):
        api = api or default_api()
        root = api.root_url
        path = "/v2/gpx/subscriptions/{0}/cancel".format(self.id)
        url = root + path
        post_data = {'seckey': api.private_key}
        headers = {
                'content-type': 'application/json',
                'accept': 'application/json'
        }
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        response = Response.from_dict(response.json())
        # TODO: remove debug print statements
        print("\n\n\n")
        print("from cancel subscription")
        print(response.status)
        print(response.message)
        print(response.data)
        print("\n\n\n")
        if response.status == RESPONSE_STATUS.SUCCESS:
            data = response.data
            self.id = data['id']
            self.amount = data['amount']
            self.customer_id = data['customer']['id']
            self.customer_email = data['customer']['customer_email']
            self.plan_id = data['plan']
            self.status = SUBSCRIPTION_STATUS(data['status'])
            self.date_created = data['date_created']
        else:
            raise RaveError(response.message)


    def activate(self, api=None):
        api = api or default_api()
        root = api.root_url
        path = "/v2/gpx/subscriptions/{0}/activate".format(self.id)
        url = root + path
        post_data = {'seckey': api.private_key}
        headers = {
                'content-type': 'application/json',
                'accept': 'application/json'
        }
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        response = Response.from_dict(response.json())
        # TODO: remove debug print statements
        print("\n\n\n")
        print("from activate subscription")
        print(response.status)
        print(response.message)
        print(response.data)
        print("\n\n\n")
        if response.status == RESPONSE_STATUS.SUCCESS:
            data = response.data
            self.id = data['id']
            self.amount = data['amount']
            self.customer_id = data['customer']['id']
            self.customer_email = data['customer']['customer_email']
            self.plan_id = data['plan']
            self.status = SUBSCRIPTION_STATUS(data['status'])
            self.date_created = data['date_created']
        else:
            raise RaveError(response.message)
