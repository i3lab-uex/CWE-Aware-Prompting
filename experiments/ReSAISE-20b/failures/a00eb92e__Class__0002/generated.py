import hmac

# Global dictionary containing the expected signatures for each message ID.
# In a real system this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg-001": "a3f5c8d2b1e4f9...",
    "msg-002": "b7e9a1c3d6f0b2...",
    # ... additional message IDs and their signatures ...
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Args:
        msg_identifier: The unique identifier of the message.
        crypto_sign: The cryptographic signature supplied with the message.

    Returns:
        True if the signatures match; False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    try:
        expected_sign = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        raise KeyError(f"Message ID '{msg_identifier}' not found in VALID_API_MESSAGES.") from exc

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(crypto_sign, expected_sign)