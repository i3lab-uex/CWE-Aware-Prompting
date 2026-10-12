import hmac

# Global dictionary containing valid message IDs and their corresponding signatures.
VALID_API_MESSAGES = {
    # Example entries; in practice these would be populated with real data.
    "msg_001": "5f2c9e8a7b3d4e6f1a0b1234567890ab",
    "msg_002": "3e4d5f6a7b8c9d0e1f2a3b4c5d6e7f80",
    # Add more message IDs and signatures as needed.
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        The identifier of the API message to validate.
    cryptographic_sign : str
        The cryptographic signature provided with the message.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the message ID exists; this raises KeyError if missing.
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sign, cryptographic_sign)