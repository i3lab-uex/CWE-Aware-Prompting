import hmac

# Example global dictionary holding the correct signatures for API messages.
# In a real system this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg-001": "a3f5c2b1d4e6f7890abcdef123456789",
    "msg-002": "b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    # Add more message identifiers and their corresponding signatures here.
}


def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the cryptographic signature supplied for a given message
    matches the expected value stored in VALID_API_MESSAGES.

    Parameters:
        msg_identifier (str): The ID of the message to verify.
        crypto_sign (str): The cryptographic signature supplied by the API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError propagates if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)