import hmac

# Global dictionary mapping message identifiers to their expected signatures.
VALID_API_MESSAGES = {
    # Example entries; in practice these would be populated from a secure source.
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "0j9i8h7g6f5e4d3c2b1a",
    # Add more entries as needed.
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The unique ID of the message to validate.
    crypto_sign : str
        The cryptographic signature supplied with the message.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' not found")

    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sign, crypto_sign)