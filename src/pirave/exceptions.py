class MissingConfigException(Exception):
    pass


class MissingArgumentException(Exception):
    pass


class InvalidArgumentException(Exception):
    pass


class TrasactionNotFoundError(Exception):
    pass


class InvalidChargeTypeError(KeyError):
    pass