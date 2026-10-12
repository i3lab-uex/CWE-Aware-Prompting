import hmac

# Example of the global dictionary containing valid signatures.
# In real usage this would be populated with actual values from your system.
VALID_API_MESSAGES = {
    # msg_id: signature
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # ... more entries ...
}


def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Args:
        msg_id: The unique identifier of the message.
        sign:   The cryptographic signature to verify.

    Returns:
        True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is unknown
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sign)