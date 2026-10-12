import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
# In a real application, this would be securely loaded from configuration or a secrets manager.
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
    # ... other message signatures ...
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        Identifier of the message to validate.
    sign : str
        Cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value; False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; KeyError propagates if not found.
    expected = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign, expected)