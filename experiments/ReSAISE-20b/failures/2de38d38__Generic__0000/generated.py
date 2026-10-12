import hmac
from typing import Dict

# Global dictionary containing valid signatures for each message code.
# Example:
# VALID_API_MESSAGES = {
#     "msg123": "5f4dcc3b5aa765d61d8327deb882cf99",
#     "msg456": "e99a18c428cb38d5f260853678922e03",
# }
VALID_API_MESSAGES: Dict[str, str] = {}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Parameters
    ----------
    msg_code : str
        Identifier of the message whose authenticity is to be verified.
    crypto_sign : str
        Cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if `crypto_sign` matches the expected signature; False otherwise.

    Raises
    ------
    KeyError
        If `msg_code` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve expected signature; raises KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)