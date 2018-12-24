import pytest

from pirave.api import Api, configure, default_api
from pirave.enums import Environment
from pirave.exceptions import MissingConfigException


def test_get_api_without_previous_config():
    with pytest.raises(MissingConfigException):
        default_api()


def test_default_api(api):
    dapi = default_api()
    assert dapi == api
    assert dapi.environment == Environment.SANDBOX


def test_configre_via_environment_variables():
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
    with pytest.raises(MissingConfigException):
        default_api()
    import os
    os.environ["RAVE_PUBLIC_KEY"] = "testpublickey"
    with pytest.raises(MissingConfigException):
        default_api()
