import hmac

# Predefined mapping of message IDs to their correct cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries; in production these would be securely stored.
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
    # ...
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the stored
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        Identifier of the message to validate.
    cryptographic_sign : str
        Cryptographic signature provided by the external API.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use a timing‑safe comparison to prevent side‑channel attacks.
    return hmac.compare_digest(cryptographic_sign, expected_sign)