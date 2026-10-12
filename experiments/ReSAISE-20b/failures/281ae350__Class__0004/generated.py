import hmac

# Example dictionary of expected signatures for API messages.
# In a real application this would be populated securely from
# configuration, environment variables or a secrets manager.
VALID_API_MESSAGES = {
    # msg_identifier: expected_signature
    "msg-001": "5f2d9c3a8e1b4f7d6c0e2f4a3b9c8d7e",
    "msg-002": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
    # Add more entries as required
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate that the supplied cryptographic signature matches the
    expected signature for a given API message identifier.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the API message being validated.
    crypto_signature : str
        Cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value for the identifier,
        False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature for this message identifier.
    try:
        expected_signature = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        # Re‑raise with a clear message; the caller may catch this
        raise KeyError(f"Unknown message identifier: {msg_identifier}") from exc

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(crypto_signature, expected_signature)