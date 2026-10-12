import hmac

# Example of predefined global dictionary holding valid signatures.
# In practice, this should be securely populated and protected.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "b2c3d4e5f6g7h8i9j0a1",
    # ... other message identifiers and their signatures
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
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not found in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; raise KeyError if not present
    try:
        expected_sign = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        raise KeyError(f"Message identifier '{msg_identifier}' not found.") from exc

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)