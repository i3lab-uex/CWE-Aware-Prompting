import hmac

# Global dictionary containing valid cryptographic signatures for API messages.
# Example format: {'msg123': 'a1b2c3d4e5f6...', ...}
VALID_API_MESSAGES = {
    # Populate with actual message-code to signature mappings.
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message code.

    Args:
        msg_code (str): Identifier of the API message.
        crypto_sign (str): Cryptographic signature supplied with the message.

    Returns:
        bool: True if the signature is valid for the given msg_code, False otherwise.

    Raises:
        KeyError: If `msg_code` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError will propagate if msg_code is missing
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Perform a timing‑attack resistant comparison.
    return hmac.compare_digest(expected_sign, crypto_sign)