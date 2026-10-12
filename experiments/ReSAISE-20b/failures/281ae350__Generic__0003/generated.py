import hmac

# Global dictionary mapping message identifiers to their expected signatures.
VALID_API_MESSAGES = {
    # Example entries; replace with actual data as needed
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef0123",
    # ...
}


def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of an external API message.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the message to validate.
    crypto_signature : str
        The signature received from the external API.

    Returns
    -------
    bool
        True if the provided signature matches the stored one, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve expected signature; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(crypto_signature, expected_signature)