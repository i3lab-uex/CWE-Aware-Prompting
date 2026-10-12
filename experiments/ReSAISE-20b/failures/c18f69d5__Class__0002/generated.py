import hmac

# Predefined mapping of message IDs to their correct cryptographic signatures.
# In a real system this would be populated from a secure source or configuration.
VALID_API_MESSAGES = {
    # Example entries
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
    # Add more message IDs and signatures as needed.
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters:
        api_message_id (str): Identifier of the message to validate.
        cryptographic_sign (str): Signature supplied by the external API.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if id is unknown
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, cryptographic_sign)