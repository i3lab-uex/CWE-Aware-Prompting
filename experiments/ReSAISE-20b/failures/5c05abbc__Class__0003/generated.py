import hmac

# Predefined dictionary of valid message IDs and their corresponding cryptographic signatures.
# In a real-world scenario, this would be securely loaded from a trusted source.
VALID_API_MESSAGES = {
    "msg001": "a1b2c3d4e5f6g7h8i9j0",
    "msg002": "1234567890abcdef1234",
    # ... additional entries ...
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored signature
    for a given message ID.

    Args:
        msg_id (str): The identifier of the message to verify.
        sign (str): The cryptographic signature claimed for that message.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; let KeyError propagate if msg_id is missing
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sign)