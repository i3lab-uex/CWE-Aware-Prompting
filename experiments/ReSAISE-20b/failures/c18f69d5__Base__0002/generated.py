import hmac

# Predefined dictionary of valid API message IDs to their cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries; replace with actual values in production
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "6c569aabbf7775ef8fc570e228c16b98",
    # ... more entries ...
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the stored
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        The identifier of the API message to validate.
    cryptographic_sign : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure that the message ID exists
    if api_message_id not in VALID_API_MESSAGES:
        raise KeyError(f"API message ID '{api_message_id}' not found.")

    # Retrieve the expected signature
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(cryptographic_sign, expected_sign)