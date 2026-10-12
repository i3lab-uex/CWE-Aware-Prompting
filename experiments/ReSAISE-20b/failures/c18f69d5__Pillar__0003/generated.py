import hmac
from typing import Dict

# Example of a global dictionary containing the expected signatures for each API message.
# In production this would be populated securely, e.g., from a database or a secrets store.
VALID_API_MESSAGES: Dict[str, str] = {
    # message_id : expected_signature
    "msg-001": "5f2c8a1b3e9d4f7e6a1b0c3d2f4e5a6b",
    "msg-002": "1a2b3c4d5e6f7g8h9i0jklmnopqrstuv",
    # ... additional entries ...
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Validate the cryptographic signature of an API message.

    Args:
        api_message_id (str): The identifier of the message.
        cryptographic_sign (str): The signature received from the external API.

    Returns:
        bool: True if the provided signature matches the stored one, False otherwise.

    Raises:
        KeyError: If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    if api_message_id not in VALID_API_MESSAGES:
        # Explicitly raise KeyError to signal unknown message ID
        raise KeyError(f"API message ID '{api_message_id}' not found in VALID_API_MESSAGES")

    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(cryptographic_sign, expected_sign)