import hmac

# Global dictionary mapping message codes to their expected cryptographic signatures.
# In a real-world scenario, these would be securely stored and protected.
VALID_API_MESSAGES = {
    # Example entries
    "msg001": "a1b2c3d4e5f6g7h8i9j0",
    "msg002": "1234567890abcdef0123",
    # Add more message codes and their corresponding signatures here.
}


def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Args:
        msg_code (str): Identifier of the message whose authenticity must be verified.
        crypto_sign (str): Cryptographic signature received from the external API.

    Returns:
        bool: True if the signature matches the expected value, False otherwise.

    Raises:
        KeyError: If `msg_code` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature for the given message code.
    # Let KeyError propagate if msg_code is missing, as required by spec.
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant‑time comparison to mitigate timing attacks (CWE-347).
    return hmac.compare_digest(expected_sign, crypto_sign)