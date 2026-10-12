import hmac

# Example global dictionary of valid API messages and their signatures.
# In a real application this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg1": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg2": "e99a18c428cb38d5f260853678922e03",
    # ... other messages
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Args:
        msg_identifier (str): Identifier of the message to verify.
        sign (str): Cryptographic signature provided by the API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError propagates if not found
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, sign)