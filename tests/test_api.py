import pytest

from pirave.api import Api, configure, default_api, reset_api
from pirave.enums import Environment
from pirave.exceptions import (InvalidEnvironmentException,
                               MissingConfigException)


def test_get_api_without_previous_config():
    reset_api()
    with pytest.raises(MissingConfigException):
        default_api()


def test_default_api(cred):
    configure(cred['public_key'], cred['private_key'])
    dcred = default_api()
    assert dcred.public_key == cred['public_key']
    assert dcred.private_key == cred['private_key']
    assert dcred.environment == Environment.SANDBOX


def test_environment_from_string():
    with pytest.raises(InvalidEnvironmentException):
        Environment.from_string("notexist")


def test_configre_via_environment_variables():
    reset_api()
    with pytest.raises(MissingConfigException):
        default_api()
    import os
    os.environ["RAVE_PUBLIC_KEY"] = "testpublickey"
    os.environ["RAVE_PRIVATE_KEY"] = "testprivatekey"
    dcred = default_api()
    assert dcred is not None
    assert dcred.environment == Environment.SANDBOX
    assert dcred.public_key == "testpublickey"
    assert dcred.private_key == "testprivatekey"


def test_configure_via_environment_vars_with_missing_vars():
    reset_api()
    with pytest.raises(MissingConfigException):
        default_api()
    import os
    os.environ["RAVE_PUBLIC_KEY"] = "testpublickey"
    with pytest.raises(MissingConfigException):
        default_api()
