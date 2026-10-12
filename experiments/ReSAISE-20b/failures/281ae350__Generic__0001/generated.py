import hmac

# Example storage of expected signatures for API messages.
# In a real application this would be populated from a secure source.
VALID_API_MESSAGES = {
    # 'msg_identifier': 'expected_signature',
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
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
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message identifier exists
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' not found")

    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use compare_digest for constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(crypto_signature, expected_signature)