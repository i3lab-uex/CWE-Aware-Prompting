import hmac

# Example global dictionary of valid signatures.
# In a real application this would be populated securely from the API provider.
VALID_API_MESSAGES = {
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # ... other messages
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters:
        msg_identifier (str): Identifier of the API message.
        sign (str): Cryptographic signature to verify.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError propagates if not found
    expected = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected)