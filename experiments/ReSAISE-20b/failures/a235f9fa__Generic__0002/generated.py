import hmac

# Example dictionary of valid signatures for API messages.
# In a real application this would be populated from secure storage.
VALID_API_MESSAGES = {
    # msg_id: signature
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # ... add more entries as needed
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature of a message received from an external API.

    Parameters
    ----------
    msg_id : str
        The identifier for the message whose authenticity needs to be checked.
    sig : str
        The cryptographic signature associated with the specified message.

    Returns
    -------
    bool
        True if the provided signature matches the stored one for `msg_id`,
        otherwise False.

    Raises
    ------
    KeyError
        If the `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve expected signature; raise KeyError if msg_id is missing
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, sig)