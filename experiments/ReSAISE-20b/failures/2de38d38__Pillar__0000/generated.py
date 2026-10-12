import hmac

# Global dictionary containing valid signatures for API messages.
# Example format:
# VALID_API_MESSAGES = {
#     "msg1": "a1b2c3d4e5f6...",
#     "msg2": "1234567890abcdef..."
# }
VALID_API_MESSAGES = {}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the
    expected signature for a given message code.

    Parameters:
        msg_code (str): Identifier of the API message.
        crypto_sign (str): Signature received from the external API.

    Returns:
        bool: True if the signature is valid for the message code, False otherwise.

    Raises:
        KeyError: If msg_code does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message code exists
    if msg_code not in VALID_API_MESSAGES:
        raise KeyError(f"Message code '{msg_code}' not found in VALID_API_MESSAGES.")

    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant-time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)