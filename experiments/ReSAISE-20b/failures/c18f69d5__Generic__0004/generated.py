import hmac

# Example dictionary of valid API message signatures.
# In production, this should be securely loaded from a protected source
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
    # ... other message IDs and their expected signatures ...
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): The ID of the message to validate.
        cryptographic_sign (str): The signature provided by the API.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if ID is unknown
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, cryptographic_sign)