import hmac

# Example dictionary mapping message codes to their valid cryptographic signatures.
# In production, this should be securely loaded from a trusted source (e.g., environment variable,
# secure vault, or compiled into the binary) and never modified at runtime.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "msg_002": "0p9o8i7h6g5f4e3d2c1b0a9j8k7l6m5n",
    # ... add more entries as needed
}


def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Args:
        msg_code (str): Identifier of the message to verify.
        crypto_sign (str): Cryptographic signature supplied with the message.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If `msg_code` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_code is unknown
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)