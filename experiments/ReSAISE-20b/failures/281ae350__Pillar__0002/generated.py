import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
# In a real application this would be populated from a secure source (e.g., a database or
# configuration file that is protected against tampering).
VALID_API_MESSAGES = {
    # Example entries; replace with actual values.
    "msg1": "a3f5c2e8b9d4e6f7c1b2a0d3e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y",
    "msg2": "b7c8d9e0f1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a",
    # Add more message identifiers and their corresponding signatures here.
}


def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of an API message.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the message being validated.
    crypto_signature : str
        The cryptographic signature provided by the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value for the given identifier,
        False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure that the identifier exists; raise KeyError if it does not.
    try:
        expected_signature = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        raise KeyError(f"Message identifier '{msg_identifier}' not found in VALID_API_MESSAGES.") from exc

    # Use hmac.compare_digest to prevent timing attacks (CWE-693).
    return hmac.compare_digest(crypto_signature, expected_signature)