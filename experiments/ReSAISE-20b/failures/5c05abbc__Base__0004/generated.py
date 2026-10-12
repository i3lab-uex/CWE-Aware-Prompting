import hmac

# Example global dictionary mapping message IDs to their valid signatures.
# In real usage this would be populated from a secure source.
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef",
    # ... more entries ...
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Parameters:
        msg_id (str): The identifier of the message to verify.
        sign (str): The cryptographic signature provided by the API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If msg_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is missing
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    return hmac.compare_digest(expected_sign, sign)