import hmac

# Example global dictionary of valid message signatures.
# In a real system this would be securely populated and stored.
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f67890123456789abcdef0",
    "msg-002": "deadbeefcafebabe1234567890abcdef",
    # ... more entries ...
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected cryptographic
    signature for the given `message_id`.

    Parameters
    ----------
    message_id : str
        The unique identifier of the message to authenticate.
    signature : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `message_id` is not present in the global VALID_API_MESSAGES map.
    """
    # Retrieve the expected signature for the message_id
    try:
        expected_sig = VALID_API_MESSAGES[message_id]
    except KeyError as exc:
        # Propagate the error with a clear message
        raise KeyError(f"Message ID '{message_id}' not found in VALID_API_MESSAGES") from exc

    # Use constant‑time comparison to mitigate timing attacks
    # Convert both signatures to bytes; assume they are hex or base64 encoded strings.
    # For safety, we use UTF‑8 encoding which will not alter the byte values of ASCII characters.
    return hmac.compare_digest(
        signature.encode("utf-8"),
        expected_sig.encode("utf-8")
    )