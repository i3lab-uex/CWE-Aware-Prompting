import hmac

# Predefined dictionary of valid message identifiers to their cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries; in production these would be securely stored and managed.
    "msg001": "a1b2c3d4e5f6g7h8i9j0",
    "msg002": "1234567890abcdef1234",
    # ... additional message identifiers and their corresponding signatures ...
}


def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The ID of the message whose authenticity needs to be verified.
    crypto_sign : str
        The cryptographic signature tied to that specific message.

    Returns
    -------
    bool
        True if the cryptographic signature matches the stored value for
        the given message ID, otherwise False.

    Raises
    ------
    KeyError
        If ``msg_identifier`` is not found in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; raise KeyError if not present
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)