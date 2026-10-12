import hmac

# Global dictionary mapping message IDs to their expected signatures.
# Example: VALID_API_MESSAGES = {"msg1": "abc123", "msg2": "def456"}
VALID_API_MESSAGES = {
    # Populate with real data in production
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected cryptographic
    signature for the given `message_id`.

    Parameters
    ----------
    message_id : str
        The unique identifier of the message.
    signature : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    KeyError
        If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, signature)