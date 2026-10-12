import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
# In a real application this should be populated from a secure source and kept confidential.
VALID_API_MESSAGES = {
    # Example entries (signature values are placeholders)
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "6b1b36c5d9d4f7e8a8e3b2cd6f1c6b12",
    # ... add more entries as needed ...
}


def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of a message from an external API.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the message to be validated.
    crypto_signature : str
        Cryptographic signature provided by the external API.

    Returns
    -------
    bool
        True if the provided signature matches the stored one for the given identifier,
        False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the global VALID_API_MESSAGES dictionary.
    """
    # Retrieve expected signature; raise KeyError if identifier is missing
    try:
        expected_signature = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        raise KeyError(f"Message identifier '{msg_identifier}' not found in VALID_API_MESSAGES.") from exc

    # Use constant‑time comparison to mitigate timing attacks (CWE‑693 consideration)
    return hmac.compare_digest(expected_signature, crypto_signature)