import hmac

# The dictionary that maps message identifiers to their expected cryptographic signatures.
# In a real application this would be populated from a secure source or configuration file.
VALID_API_MESSAGES = {
    # Example entries:
    # "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    # "msg_002": "1a2b3c4d5e6f7g8h9i0j",
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored value for
    a given message identifier.

    Parameters:
        msg_identifier (str): The ID of the message to verify.
        crypto_sign (str): The cryptographic signature supplied by the external API.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    try:
        expected_sign = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        raise KeyError(f"Message identifier '{msg_identifier}' not found.") from exc

    # Use a constant‑time comparison to mitigate timing attacks (CWE‑693)
    return hmac.compare_digest(expected_sign, crypto_sign)