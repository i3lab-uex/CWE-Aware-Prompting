import hmac

# Example global dictionary mapping message IDs to their correct signatures.
VALID_API_MESSAGES = {
    # "message_id": "expected_signature",
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "b1c2d3e4f5g6h7i8j9k0",
    # Add more entries as needed
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the stored
    value for the given API message ID.

    Args:
        api_message_id: Identifier of the API message.
        cryptographic_sign: Signature supplied with the message.

    Returns:
        True if signatures match, False otherwise.

    Raises:
        KeyError: If the api_message_id is not present in VALID_API_MESSAGES.
    """
    if api_message_id not in VALID_API_MESSAGES:
        # Explicitly raise KeyError to signal missing message ID
        raise KeyError(f"API message ID '{api_message_id}' not found")

    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, cryptographic_sign)