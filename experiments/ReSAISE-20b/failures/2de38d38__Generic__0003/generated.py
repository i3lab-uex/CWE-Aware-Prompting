import hmac

# Example global dictionary of valid signatures for API messages.
# In real usage, this should be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "6c1b2e3d4f5a6b7c8d9e0f1122334455",
    # ... other message codes and their expected signatures
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Args:
        msg_code (str): Identifier of the message.
        crypto_sign (str): Signature received from the external API.

    Returns:
        bool: True if signatures match, False otherwise.

    Raises:
        KeyError: If msg_code is not present in VALID_API_MESSAGES.
    """
    # Ensure the message code exists; otherwise raise KeyError
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Convert both signatures to bytes for a secure comparison.
    # Using UTF-8 encoding is standard; adjust if your signatures use another format.
    expected_bytes = expected_sign.encode('utf-8')
    received_bytes = crypto_sign.encode('utf-8')

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_bytes, received_bytes)