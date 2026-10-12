import secrets

# Example predefined global dictionary of valid API messages.
# In a real application, this would be populated from secure storage or environment variables.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # Add more message IDs and their corresponding cryptographic signatures here.
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Validate the authenticity of an API message by comparing its cryptographic signature
    with a pre‑stored value.

    Parameters
    ----------
    api_message_id : str
        The unique identifier of the message to validate.
    cryptographic_sign : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value for the given message ID,
        False otherwise.

    Raises
    ------
    KeyError
        If the provided `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure that the message ID exists; raise KeyError if not found
    stored_sign = VALID_API_MESSAGES[api_message_id]  # This will raise KeyError if missing

    # Use a constant‑time comparison to mitigate timing attacks
    return secrets.compare_digest(stored_sign, cryptographic_sign)