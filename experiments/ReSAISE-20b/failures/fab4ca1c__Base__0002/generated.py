import hmac
from typing import Dict

# Example global dictionary containing valid signatures for API messages.
# In a real application, this would be populated securely from a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    # 'message_id': 'hex_encoded_signature',
    "msg_001": "5f2c1a3e9b7d4e8f6a2b0c1d3e5f6789",
    "msg_002": "a1b2c3d4e5f67890123456789abcdef0",
    # ... add more entries as needed
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Args:
        msg_identifier: Identifier of the API message to validate.
        sign: The cryptographic signature provided with the message.

    Returns:
        True if the signatures match, False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Ensure the identifier exists; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use hmac.compare_digest to avoid timing attacks.
    return hmac.compare_digest(sign, expected_sign)