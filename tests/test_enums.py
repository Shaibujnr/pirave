import pytest
from pirave.enums import Environment
from pirave.exceptions import InvalidEnvironmentException


def test_from_string_with_non_existing():
    with pytest.raises(InvalidEnvironmentException):
        Environment.from_string('non_existing')


def test_from_string():
    env = Environment.from_string("sandbox")
    env2 = Environment.from_string("live")
    assert env == Environment.SANDBOX
    assert env2 == Environment.LIVE
