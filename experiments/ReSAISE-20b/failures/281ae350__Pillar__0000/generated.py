import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries (should be populated with real data in production)
    "msg_001": "a3f5c2e1b9d4...",
    "msg_002": "7c8a12f0e3b9...",
    # ...
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of an API message.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the message to validate.
    crypto_signature : str
        Signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value for the given identifier,
        False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Ensure the identifier exists; raise KeyError if missing
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to prevent timing attacks (CWE‑693 mitigation)
    return hmac.compare_digest(crypto_signature, expected_signature)

# Example usage (commented out for safety):
# try:
#     result = validate_api_message("msg_001", "a3f5c2e1b9d4...")
#     print("Signature valid:", result)
# except KeyError:
#     print("Unknown message identifier.")