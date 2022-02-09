import base64
from framework.utils.logger import Logger


def base64_decode(b64_message):
    """The function takes a byte string in Base64 format and decodes it to UTF-8"""
    Logger.info("Decoding b64 to utf-8")
    message = base64.urlsafe_b64decode(
        b64_message + '=' * (-len(b64_message) % 4)).decode(encoding='utf-8')
    return message
