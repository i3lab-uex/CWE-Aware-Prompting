import hmac

# Example of the global dictionary that maps message IDs to their valid signatures.
# In a real application this would be securely loaded from a trusted source.
VALID_API_MESSAGES = {
    "msg_001": "a3f9c2d8e1b4c6d7f0e5a12345678901",
    "msg_002": "b4c6d7f0e5a12345678901a3f9c2d8e1b",
    # ... other message IDs and their corresponding signatures ...
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Validate the cryptographic signature of an API message.

    Parameters
    ----------
    api_message_id : str
        The ID of the message whose authenticity needs to be verified.
    cryptographic_sign : str
        The cryptographic signature tied to that specific message.

    Returns
    -------
    bool
        True if the provided signature matches the stored value for the given message ID,
        otherwise False.

    Raises
    ------
    KeyError
        If the api_message_id is not found in VALID_API_MESSAGES.
    """
    if api_message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{api_message_id}' is unknown")

    expected_sign = VALID_API_MESSAGES[api_message_id]
    # Use constant-time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sign, cryptographic_sign)