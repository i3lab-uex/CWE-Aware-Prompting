import hmac

# Global dictionary containing valid signatures for API messages.
# Example: {'msg123': 'a1b2c3d4e5f6...', ...}
VALID_API_MESSAGES = {
    # Populate with real values in production
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Args:
        msg_identifier (str): Identifier of the message.
        sign (str): Cryptographic signature to verify.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Ensure both signatures are bytes for compare_digest
    if isinstance(sign, str):
        sign_bytes = sign.encode('utf-8')
    else:
        sign_bytes = sign

    if isinstance(expected_sign, str):
        expected_bytes = expected_sign.encode('utf-8')
    else:
        expected_bytes = expected_sign

    # Constant-time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(sign_bytes, expected_bytes)