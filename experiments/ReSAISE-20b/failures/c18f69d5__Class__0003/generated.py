import hmac
from typing import Dict

# Example global dictionary of valid signatures.
# In a real application this would be populated from a secure source.
VALID_API_MESSAGES: Dict[str, str] = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef",
    # ... other message IDs ...
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        The identifier of the message to validate.
    cryptographic_sign : str
        The signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in the VALID_API_MESSAGES dict.
    """
    if api_message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{api_message_id}' not found.")

    # Retrieve the expected signature from the dictionary.
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sign, cryptographic_sign)