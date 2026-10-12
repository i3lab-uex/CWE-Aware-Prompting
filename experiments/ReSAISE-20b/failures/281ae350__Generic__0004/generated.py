import hmac

# Global dictionary containing the expected cryptographic signatures for each message identifier.
VALID_API_MESSAGES = {
    # Example entries (to be replaced with real data)
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # Add more message identifiers and their expected signatures here
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of an external API message.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the message being checked.
    crypto_signature : str
        The cryptographic signature to validate against the stored signature.

    Returns
    -------
    bool
        True if the provided signature matches the expected one, False otherwise.

    Raises
    ------
    KeyError
        If ``msg_identifier`` is not present in :data:`VALID_API_MESSAGES`.
    """
    # Retrieve the expected signature for this message identifier.
    try:
        expected_signature = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        # Explicitly raise a KeyError if the identifier is missing.
        raise KeyError(f"Message identifier '{msg_identifier}' not found.") from exc

    # Use hmac.compare_digest for a timing‑attack resistant comparison.
    return hmac.compare_digest(crypto_signature, expected_signature)