import hmac
from typing import Dict

# Example of the predefined dictionary. In practice this would be populated with real data.
VALID_API_MESSAGES: Dict[str, str] = {
    # "msg_id": "signature",
    # e.g. "12345": "a1b2c3d4e5f6...",
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Args:
        msg_id (str): The ID of the message to verify.
        sign (str): The cryptographic signature received from the API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError will propagate if missing
    expected = VALID_API_MESSAGES[msg_id]

    # Ensure both signatures are of the same type (bytes) for compare_digest
    if isinstance(sign, str):
        sign_bytes = sign.encode('utf-8')
    else:
        sign_bytes = sign

    if isinstance(expected, str):
        expected_bytes = expected.encode('utf-8')
    else:
        expected_bytes = expected

    # Constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sign_bytes, expected_bytes)