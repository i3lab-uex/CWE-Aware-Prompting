import hmac

# Global dictionary containing expected signatures for API messages.
# Example structure: {"msg123": "a1b2c3d4...", ...}
VALID_API_MESSAGES = {
    # Populate with actual message IDs and signatures as needed.
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for the given message_id.

    Parameters:
        message_id (str): Unique identifier of the API message.
        signature (str): Cryptographic signature supplied by the external API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If message_id does not exist in VALID_API_MESSAGES.
    """
    if message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{message_id}' not found.")

    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant-time comparison to mitigate timing attacks (CWE-693).
    return hmac.compare_digest(expected_sig, signature)