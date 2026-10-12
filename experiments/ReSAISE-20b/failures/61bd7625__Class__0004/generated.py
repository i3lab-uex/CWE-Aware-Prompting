import hmac

# Global dictionary mapping message IDs to their expected signatures.
# Example: VALID_API_MESSAGES = {"msg123": "5f2c..."}
VALID_API_MESSAGES = {
    # Populate with actual message_id: signature pairs
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected
    signature for the given `message_id`.

    Parameters
    ----------
    message_id : str
        The unique identifier of the API message.
    signature : str
        The cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message exists
    if message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{message_id}' not found.")

    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(signature, expected_sig)