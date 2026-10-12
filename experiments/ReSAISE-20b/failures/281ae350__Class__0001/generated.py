import hmac

# Example global dictionary of valid signatures for each message identifier.
# In a real system this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg1": "a3f5c2d9e8b7",
    "msg2": "4b6a1f0c3d9e",
    # ... more entries ...
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of an external API message.

    Parameters
    ----------
    msg_identifier : str
        A unique identifier for the message being checked.
    crypto_signature : str
        The cryptographic signature to validate.

    Returns
    -------
    bool
        True if the signature matches the stored one for the given identifier,
        False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` does not exist in VALID_API_MESSAGES.
    """
    # Ensure the identifier exists; raise KeyError if missing
    expected_sig = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sig, crypto_signature)