import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
# In a real application this would be securely stored and possibly refreshed regularly.
VALID_API_MESSAGES = {
    # Example entries
    "msg001": "a1b2c3d4e5f67890abcdef1234567890",
    "msg002": "0123456789abcdef0123456789abcdef",
    # ... add real signatures here
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_code : str
        The identifier of the message whose authenticity must be verified.
    crypto_sign : str
        The cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value for ``msg_code``;
        otherwise False.

    Raises
    ------
    KeyError
        If ``msg_code`` is not present in the VALID_API_MESSAGES dictionary.
    """
    if msg_code not in VALID_API_MESSAGES:
        # Explicitly raise KeyError to signal unknown message identifiers
        raise KeyError(f"Message code '{msg_code}' not found in VALID_API_MESSAGES")

    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant‑time comparison to mitigate timing attacks (CWE‑693).
    return hmac.compare_digest(expected_sign, crypto_sign)