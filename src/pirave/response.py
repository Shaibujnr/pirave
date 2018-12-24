from .enums import RESPONSE_STATUS

class Response:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self. data = data

    @classmethod
    def from_dict(cls, response_dict):
        return cls(
            RESPONSE_STATUS(response_dict['status']),
            response_dict['message'],
            response_dict['data']
        )