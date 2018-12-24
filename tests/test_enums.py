import pytest
from pirave.enums import Environment


def test_with_non_existing():
    with pytest.raises(ValueError):
        Environment('non_existing')


def test_environment_enum():
    env = Environment("sandbox")
    env2 = Environment("live")
    assert env == Environment.SANDBOX
    assert env2 == Environment.LIVE
