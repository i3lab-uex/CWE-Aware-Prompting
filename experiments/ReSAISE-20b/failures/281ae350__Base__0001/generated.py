import hmac

# Global dictionary mapping message identifiers to their expected signatures.
# In a real application, this would be securely populated from a trusted source.
VALID_API_MESSAGES = {
    "msg_001": "5f2c3a1b4e6d7f8g9h0i",
    "msg_002": "a1b2c3d4e5f6g7h8i9j0",
    # Add more entries as needed.
}


def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the stored
    expected signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier of the API message.
    crypto_signature : str
        Cryptographic signature to be validated.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing.
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to avoid timing attacks (CWE-347).
    return hmac.compare_digest(expected_signature, crypto_signature)