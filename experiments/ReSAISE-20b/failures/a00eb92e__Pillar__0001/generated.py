import hmac
from typing import Dict

# Example global dictionary containing valid message IDs and their signatures.
# In a real application this would be securely populated from a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "0123456789abcdef1234",
    # ... more entries ...
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Args:
        msg_identifier (str): The ID of the message to verify.
        crypto_sign (str): The cryptographic signature received from the API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError will propagate if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(expected_sign, crypto_sign)