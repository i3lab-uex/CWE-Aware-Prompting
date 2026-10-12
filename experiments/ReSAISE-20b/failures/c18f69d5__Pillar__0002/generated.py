import hmac

# Predefined mapping of message IDs to their expected cryptographic signatures.
# In a real application this would be securely stored and managed.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # ... additional entries ...
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): The identifier of the API message.
        cryptographic_sign (str): The signature supplied with the message.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If the api_message_id does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, cryptographic_sign)