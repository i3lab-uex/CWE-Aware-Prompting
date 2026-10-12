import hmac

# Global dictionary mapping message identifiers to their valid signatures.
# In a real application this would be securely stored and possibly encrypted.
VALID_API_MESSAGES = {
    "msg001": "a1b2c3d4e5f6g7h8i9j0",
    "msg002": "0123456789abcdef1234",
    # ... additional entries ...
}


def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        Identifier of the API message to validate.
    sign : str
        Signature provided by the external API.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in ``VALID_API_MESSAGES``.
    """
    if msg_identifier not in VALID_API_MESSAGES:
        # Explicitly raise KeyError to signal unknown message identifier
        raise KeyError(f"Unknown message identifier: {msg_identifier}")

    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sign, sign)