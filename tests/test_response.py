import pytest
from pirave.response import Response
from pirave.enums import RAVERESPONSE

def test_response_from_dict():
    response_dict = {
        "status":"success",
        "message":"AUTH_SUGGESTION",
        "data":{"suggested_auth":"PIN"}
    }
    response = Response.from_dict(response_dict)
    assert response is not None
    assert response.status == RAVERESPONSE.SUCCESS
    assert isinstance(response.data, dict)
    