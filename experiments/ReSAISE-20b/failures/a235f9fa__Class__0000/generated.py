import hmac

# Global dictionary mapping message IDs to their valid cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries (signature strings are placeholders)
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef",
    # Add real signatures here
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate that the provided cryptographic signature `sig` matches the
    expected signature for the given message identifier `msg_id`.

    Parameters
    ----------
    msg_id : str
        Identifier of the message to validate.
    sig : str
        Cryptographic signature supplied with the message.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    KeyError
        If `msg_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the message ID exists; otherwise raise KeyError
    if msg_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{msg_id}' not found")

    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, sig)