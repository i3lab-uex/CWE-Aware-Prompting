import hmac

# Example dictionary of valid cryptographic signatures for API messages.
# In a real system this would be populated from secure storage or a database.
VALID_API_MESSAGES = {
    "msg-001": "a3f5c8d1e2b4f6c9a7d0e1b3c5f8d2a0",
    "msg-002": "b4e1d9c7f6a2b3d5e8c0f1a4b6d9c3e7",
    # ... more message IDs and their expected signatures ...
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): The identifier of the incoming message.
        cryptographic_sign (str): The signature received from the external API.

    Returns:
        bool: True if the signature matches the stored value, False otherwise.

    Raises:
        KeyError: If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if id is unknown
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sign, cryptographic_sign)