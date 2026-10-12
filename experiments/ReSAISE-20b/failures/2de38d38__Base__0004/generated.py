import hmac

# Example global dictionary of valid signatures for API messages.
# In a real application, this would be securely loaded from a trusted source.
VALID_API_MESSAGES = {
    "msg001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg002": "e99a18c428cb38d5f260853678922e03",
    # ... more entries ...
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message code.

    Args:
        msg_code (str): Identifier of the message.
        crypto_sign (str): Hexadecimal cryptographic signature supplied by the API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If msg_code is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    return hmac.compare_digest(expected_sign, crypto_sign)