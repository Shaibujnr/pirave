import time
import base64
import hashlib
from Crypto.Cipher import DES3
from .exceptions import MissingArgumentException, InvalidArgumentException


def validate_params(params, guides):
    data = {}
    try:
        for guide in guides:

            data[guide[0]] = params[guide[1]] if guide[2] else params.get(guide[1], guide[3])
            if guide[1] in params:
                del params[guide[1]]
    except KeyError as e:
        print("\n\n\n%s argument is missing\n\n\n"%e)
        raise MissingArgumentException(str(e))
    if params:
        raise InvalidArgumentException()
    return {k:v for k,v in data.items() if bool(v)}


def get_time_ms():
    return str(int(round(time.time() * 1000)))


# Rave encryption
def encrypt_data(plainText, private_key):
    """
    encrypts your payload by using plaintext and generated encryption Key.
    """
    def get_encryption_key():
        """
        generates an encryption Key for you by using secret key
        """
        seckey = private_key
        hashedseckey = hashlib.md5(seckey.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = seckey.replace('FLWSECK-', '')
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        return seckeyadjustedfirst12 + hashedseckeylast12
    key = get_encryption_key()
    blockSize = 8
    padDiff = blockSize - (len(plainText) % blockSize)
    cipher = DES3.new(key, DES3.MODE_ECB)
    plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
    return base64.b64encode(cipher.encrypt(plainText)).decode('utf-8')