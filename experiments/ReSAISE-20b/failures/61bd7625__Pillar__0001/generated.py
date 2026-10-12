import hmac

# Example global dictionary mapping message IDs to their expected signatures.
# In a real system this would be securely stored and retrieved from a
# protected data store rather than hard‑coded.
VALID_API_MESSAGES = {
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # ... additional entries ...
}


def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected signature for
    `message_id`.

    Parameters
    ----------
    message_id : str
        Unique identifier of the message.
    signature : str
        Cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature. Raise KeyError if not found.
    try:
        expected_sig = VALID_API_MESSAGES[message_id]
    except KeyError as exc:
        raise KeyError(f"Message ID '{message_id}' not found.") from exc

    # Use constant‑time comparison to mitigate timing attacks (CWE-693).
    return hmac.compare_digest(signature, expected_sig)