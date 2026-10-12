import hmac

# Predefined dictionary containing the correct signatures for each message ID.
# In a real system this would be loaded securely from a protected store.
VALID_API_MESSAGES = {
    "msg001": "5f2d4e9a1c3b8e6f7d0c2b1a4f9e3d5c",
    "msg002": "9a7b1c2d4e3f5g6h8i0j1k2l3m4n5o6p",
    # ... more message IDs and their expected signatures
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        msg_id (str): The identifier of the message.
        sign (str): The cryptographic signature to verify.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is unknown
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, sign)