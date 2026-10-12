import hmac

# Global dictionary mapping message IDs to their valid signatures.
# In a real application this would be securely populated from the API provider.
VALID_API_MESSAGES = {
    # Example entries (replace with real values)
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "abcdef1234567890fedcba",
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the
    expected signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        Identifier of the message whose authenticity is to be verified.
    sig : str
        Signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    KeyError
        If ``msg_id`` is not present in :data:`VALID_API_MESSAGES`.
    """
    # Ensure the message ID exists; this will raise KeyError if not found.
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sig, expected_sig)