import os
from .enums import Environment
from  .exceptions import MissingConfigException

class Api:
    """Api class for Rave credentials

    Args:
        public_key (str): Rave public key
        private_key (str): Rave secret key
        environment (Environment): Rave environment, either sandbox/test or live

    Attributes:
        public_key (str): Rave public key
        private_key (str): Rave secret key
        environment (Environment, optional): Rave environment, either sandbox/test or live

    """
    def __init__(self, public_key, private_key, environment=Environment.SANDBOX):
        self.environment = environment
        self.public_key = public_key
        self.private_key = private_key


    @property
    def root_url(self):
        """str: returns the root url making request to rave based on environment"""
        __path_environment_mapping = {
            Environment.LIVE: "https://api.ravepay.co",
            Environment.SANDBOX: "https://ravesandboxapi.flutterwave.com"
        }
        return __path_environment_mapping[self.environment]



__api__ = None


def configure(public_key, private_key, environment=Environment.SANDBOX):
    """This is a function to configure the rave api

    Args:
        public_key (str): Rave public key
        private_key (str): Rave secret key
        environment (Environment): Rave environment, either sandbox/test or live

    Returns:
        obj: Api if successful, False otherwise.

    """
    global __api__
    __api__ = Api(public_key, private_key, environment)
    return __api__


def default_api():
    """This is a function to fetch the default api

    Returns:
        obj: Api if has been configured or environment variables are set

    Raises:
        MissingConfigException: If configuring via environment variables and
            either RAVE_PUBLIC or RAVE_PRIVATE_KEY is missing.
        InvalidEnvironmentException: If configuring via environment variables
            and a value other than 'sandbox' or 'live' is stored as
            RAVE_ENVIRONMENT

    """
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
