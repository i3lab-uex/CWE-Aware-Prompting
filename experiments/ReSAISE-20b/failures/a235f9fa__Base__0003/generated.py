import hmac

# Global dictionary mapping message IDs to their expected cryptographic signatures.
# In a real application this would be populated from a secure source.
VALID_API_MESSAGES = {
    # Example entries:
    # "msg123": "a1b2c3d4e5f6...",
    # "msg456": "0f1e2d3c4b5a..."
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        Identifier of the API message.
    sig : str
        Signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the expected value for `msg_id`,
        False otherwise.

    Raises
    ------
    KeyError
        If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is missing
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)