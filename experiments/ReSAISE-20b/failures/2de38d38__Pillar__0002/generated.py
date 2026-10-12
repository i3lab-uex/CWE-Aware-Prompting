import hmac
from typing import Dict

# Example global dictionary storing valid signatures for API messages.
# In a real application this would be populated securely from a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    "msg001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg002": "e99a18c428cb38d5f260853678922e03",
    # ... other message signatures
}


def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Args:
        msg_code: Identifier of the API message.
        crypto_sign: Cryptographic signature supplied by the external API.

    Returns:
        True if the signature is valid for the message code, False otherwise.

    Raises:
        KeyError: If msg_code does not exist in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_code is unknown
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)