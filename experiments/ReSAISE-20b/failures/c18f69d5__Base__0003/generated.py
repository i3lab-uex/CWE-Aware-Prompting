import hmac

# Global dictionary mapping message IDs to their correct signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with real values in production)
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "b1c2d3e4f5g6h7i8j9k0",
    # ... additional entries ...
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the one stored
    for the given API message ID.

    Args:
        api_message_id (str): The identifier of the message to validate.
        cryptographic_sign (str): The signature received from the external API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    try:
        expected_sign = VALID_API_MESSAGES[api_message_id]
    except KeyError as exc:
        raise KeyError(f"Message ID '{api_message_id}' not found.") from exc

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(cryptographic_sign, expected_sign)