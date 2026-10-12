import hmac

# Global dictionary containing expected signatures for API messages.
# Example structure: {'msg123': 'a1b2c3d4...', ...}
VALID_API_MESSAGES = {
    # Populate with actual message_id:signature pairs as needed
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected signature for
    `message_id` from VALID_API_MESSAGES.

    Parameters
    ----------
    message_id : str
        Unique identifier of the message to authenticate.
    signature : str
        Cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    return hmac.compare_digest(expected_sig, signature)