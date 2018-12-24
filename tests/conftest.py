import pytest
from pirave.api import reset_api, configure

@pytest.fixture()
def api():
    return configure(
        "FLWPUBK-bd9d909913d62af9b96cfdec5118bcda-X",
        "FLWSECK-e999f602e9cc023fce7fdd44593f55e8-X"
    )


@pytest.fixture(autouse=True)
def no_api():
    reset_api()
    return None