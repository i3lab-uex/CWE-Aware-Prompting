import hmac

# Example global dictionary of valid API messages and their signatures.
# In a real application this would be populated from a secure source.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef",
    # ... additional message identifiers and signatures ...
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for the given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The unique ID of the message to verify.
    crypto_sign : str
        The cryptographic signature supplied with the message.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature for the given message identifier.
    try:
        expected_sign = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        # Propagate a clear error message.
        raise KeyError(f"Message identifier '{msg_identifier}' not found.") from exc

    # Use a timing‑attack resistant comparison.
    return hmac.compare_digest(
        expected_sign.encode("utf-8"),
        crypto_sign.encode("utf-8")
    )