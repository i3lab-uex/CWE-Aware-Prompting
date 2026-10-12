import hmac

# Predefined dictionary mapping message IDs to their correct cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries; replace with actual values in production
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "b2c3d4e5f6g7h8i9j0a1",
    # ...
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Parameters:
        msg_id (str): The identifier of the message to verify.
        sign (str): The cryptographic signature supplied by the external API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError will propagate if missing
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(sign, expected_sign)