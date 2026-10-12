import hmac

# Global dictionary containing expected cryptographic signatures for API messages.
# Example structure: {'msg_id_1': 'signature1', 'msg_id_2': 'signature2', ...}
VALID_API_MESSAGES = {
    # Populate with real signatures in production
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of a message received from an external API.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the message being checked.
    crypto_signature : str
        The cryptographic signature to validate against the stored value.

    Returns
    -------
    bool
        True if the signature matches the expected value for ``msg_identifier``,
        False otherwise.

    Raises
    ------
    KeyError
        If ``msg_identifier`` does not exist in the global VALID_API_MESSAGES dict.
    """
    # Ensure the message identifier exists
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' is unknown.")

    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to avoid timing attacks (CWE-347).
    return hmac.compare_digest(expected_signature, crypto_signature)