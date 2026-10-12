import hmac

# Global dictionary mapping message identifiers to their expected signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with real data in production)
    "msg_001": "d2c7e8a9f3b1...",
    "msg_002": "4a6f7c8d9e0b...",
    # ...
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of an API message.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the message being verified.
    crypto_signature : str
        Signature supplied by the external API to be checked.

    Returns
    -------
    bool
        True if the signature matches the stored one, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve expected signature; raise KeyError if not found
    try:
        expected_signature = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        raise KeyError(f"Message identifier '{msg_identifier}' not found.") from exc

    # Use constant-time comparison to avoid timing attacks (CWE-347 mitigation)
    return hmac.compare_digest(expected_signature, crypto_signature)