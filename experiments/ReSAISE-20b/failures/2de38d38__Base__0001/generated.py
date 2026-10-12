import hmac
from typing import Dict

# Global dictionary containing valid signatures for API messages.
# Example: VALID_API_MESSAGES = {"msg1": "signature1", "msg2": "signature2"}
VALID_API_MESSAGES: Dict[str, str] = {}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message code.

    Args:
        msg_code: Identifier of the message to validate.
        crypto_sign: Signature received from the external API.

    Returns:
        True if the signature matches; False otherwise.

    Raises:
        KeyError: If `msg_code` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature. Raises KeyError if missing.
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant‑time comparison to prevent timing attacks.
    return hmac.compare_digest(expected_sign, crypto_sign)