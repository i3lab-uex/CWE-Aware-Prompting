import hmac

# Example global dictionary mapping message codes to their expected signatures.
# In a real application, this would be populated from a secure source.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # Add more entries as needed
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for a given message code.

    Args:
        msg_code (str): Identifier of the message.
        crypto_sign (str): Signature received from the external API.

    Returns:
        bool: True if signatures match, False otherwise.

    Raises:
        KeyError: If msg_code is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)