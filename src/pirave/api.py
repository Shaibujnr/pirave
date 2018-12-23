import os
from .enums import Environment
from  .exceptions import MissingConfigException

class Api:
    def __init__(self, public_key, private_key, environment=Environment.SANDBOX):
        self.environment = environment
        self.public_key = public_key
        self.private_key = private_key

__api__ = None


def configure(public_key, private_key, environment=Environment.SANDBOX):
    global __api__
    __api__ = Api(public_key, private_key, environment)
    return __api__


def default_api():
    global __api__
    if __api__ is None:
        try:
            public_key = os.environ["RAVE_PUBLIC_KEY"]
            private_key = os.environ["RAVE_PRIVATE_KEY"]
        except KeyError:
            raise MissingConfigException("Required RAVE_PUBLIC_KEY and RAVE_PRIVATE_KEY")

        environment = Environment.from_string(os.environ.get("RAVE_ENVIRONMENT", "sandbox"))
        __api__ = Api(public_key, private_key, environment)
    return __api__


def reset_api():
    global __api__
    __api__ = None
    try:
        del os.environ["RAVE_PUBLIC_KEY"]
        del os.environ["RAVE_PRIVATE_KEY"]
        del os.environ["RAVE_ENVIRONMENT"]
    except KeyError:
        pass
