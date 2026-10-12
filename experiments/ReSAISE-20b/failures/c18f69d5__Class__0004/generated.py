import hmac

# Example dictionary of valid message IDs to their cryptographic signatures.
# In production, this would be securely populated from a trusted source.
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
    # ... more entries ...
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    value for the given message ID.

    Parameters
    ----------
    api_message_id : str
        The unique identifier of the API message.
    cryptographic_sign : str
        The signature received from the external source.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If ``api_message_id`` is not present in the global VALID_API_MESSAGES dict.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to prevent timing attacks
    return hmac.compare_digest(cryptographic_sign, expected_sign)