import hmac

# Global dictionary holding the expected signatures for each message identifier.
# Example structure: {"msg1": "signature_value", ...}
VALID_API_MESSAGES = {
    # These should be populated with real, securely stored signatures.
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of a message received from an external API.

    Parameters
    ----------
    msg_identifier : str
        A unique identifier for the message being checked.
    crypto_signature : str
        The cryptographic signature that needs to be validated against the stored signature.

    Returns
    -------
    bool
        True if the provided signature matches the expected one for the given identifier,
        False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the identifier exists; raise KeyError if it does not
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' is unknown.")

    # Retrieve the expected signature
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)