import secrets

# Example dictionary of valid signatures for API messages.
# In a real system this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "0123456789abcdef1234",
    # Add more message identifiers and their expected signatures here.
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of an external API message.

    Parameters
    ----------
    msg_identifier : str
        A unique identifier for the message being checked.
    crypto_signature : str
        The cryptographic signature to validate against the stored value.

    Returns
    -------
    bool
        True if the signature matches the expected value for the given identifier,
        otherwise False.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message identifier exists; raise KeyError if not.
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to mitigate timing attacks.
    return secrets.compare_digest(expected_signature, crypto_signature)