import hmac

# Global dictionary of expected signatures for each message ID.
# In a real application this would be populated securely, e.g. from
# a database or an environment variable.
VALID_API_MESSAGES = {
    # Example entries:
    "msg_001": "5f2d3a1b4c6e7f8g9h0i",
    "msg_002": "a1b2c3d4e5f60718293a",
    # Add additional message IDs and their expected signatures here.
}


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the
    expected signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        Unique identifier of the API message.
    crypto_signature : str
        Cryptographic signature to validate.

    Returns
    -------
    bool
        True if the signature is valid for the message ID, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    if api_message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown API message ID: {api_message_id}")

    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_signature, crypto_signature)