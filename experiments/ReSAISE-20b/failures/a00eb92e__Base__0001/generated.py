import hmac

# Example of predefined global dictionary containing correct signatures.
# In a real system this would be populated from a secure source.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f67890",
    "msg_002": "0f1e2d3c4b5a6978",
    # Add more message IDs and their signatures here
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Args:
        msg_identifier (str): The ID of the message to verify.
        crypto_sign (str): The cryptographic signature provided by the API.

    Returns:
        bool: True if signatures match, False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)