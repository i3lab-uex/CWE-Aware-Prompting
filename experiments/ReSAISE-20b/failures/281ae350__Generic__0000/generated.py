import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries – replace with actual data as needed
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef",
    # ...
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier of the API message.
    crypto_signature : str
        Cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the identifier exists; let KeyError propagate with a clear message
    try:
        expected_signature = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        raise KeyError(f"Message identifier '{msg_identifier}' not found.") from exc

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)