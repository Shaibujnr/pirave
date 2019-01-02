import enum

class Environment(enum.Enum):
    SANDBOX = "sandbox"
    LIVE = "live"


class RESPONSE_STATUS(enum.Enum):
    SUCCESS = "success"
    ERROR = "error"


class SUGGESTED_AUTH(enum.Enum):
    PIN = "PIN"
    NOAUTH_INTERNATIONAL = "NOAUTH_INTERNATIONAL"
    AVS_VBVSECURECODE = "AVS_VBVSECURECODE"


class TRANSACTION_STATUS(enum.Enum):
    SUCCESS = "successful"
    FAILED = "failed"
    PENDING = "success-pending-validation"


class CHARGE(enum.Enum):
    CARD = "card"
    ACCOUNT = "account"


class PAYMENT_PLAN_STATUS(enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


class SUBSCRIPTION_STATUS(enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
