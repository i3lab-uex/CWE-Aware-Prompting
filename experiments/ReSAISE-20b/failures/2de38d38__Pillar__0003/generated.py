import hmac

# Example global dictionary of valid API message signatures.
# In production, this would be populated securely and kept confidential.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "b1c2d3e4f5g6h7i8j9k0",
    # ... additional entries ...
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Args:
        msg_code (str): Identifier of the API message.
        crypto_sign (str): Signature supplied with the message.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If msg_code does not exist in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_code is missing
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)