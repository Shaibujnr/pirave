class RaveError(Exception):
    pass
    
class MissingConfigException(RaveError):
    pass


class MissingArgumentException(RaveError):
    pass


class InvalidArgumentException(RaveError):
    pass


class TrasactionNotFoundError(RaveError):
    pass


class InvalidChargeTypeError(RaveError):
    pass
