import enum
from .exceptions import InvalidEnvironmentException

class Environment(enum.Enum):
    SANDBOX = 1
    LIVE = 2

    @classmethod
    def from_string(cls, string):
        if string == "sandbox":
            return cls.SANDBOX
        elif string == "live":
            return cls.LIVE
        else:
            raise InvalidEnvironmentException("%s is not a valid environment type"%string)


class RAVERESPONSE(enum.Enum):
    SUCCESS = 1
    ERROR = 2

    @classmethod
    def from_string(cls, string):
        if string == "success":
            return cls.SUCCESS
        elif string == "error":
            return cls.ERROR