import hmac

# Example global dictionary containing valid signatures for API messages.
# In a real scenario, this would be populated from a secure source.
VALID_API_MESSAGES = {
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # ... more entries
}


def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for the given message code.

    Args:
        msg_code (str): Identifier of the message to validate.
        crypto_sign (str): Cryptographic signature provided by the API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `msg_code` does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message code exists; let KeyError propagate if not.
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use hmac.compare_digest for a timing‑attack resistant comparison.
    return hmac.compare_digest(expected_sign, crypto_sign)