import secrets

# Example dictionary containing valid signatures for API messages.
# In real usage this should be populated securely, e.g. from a database or environment variable.
VALID_API_MESSAGES = {
    "msg_001": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "msg_002": "5d41402abc4b2a76b9719d911017c592",
    # Add more message IDs and their expected cryptographic signatures here.
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        The identifier of the API message to validate.
    cryptographic_sign : str
        The cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; let KeyError propagate if not found
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use a constant‑time comparison to avoid timing attacks
    return secrets.compare_digest(cryptographic_sign, expected_sign)