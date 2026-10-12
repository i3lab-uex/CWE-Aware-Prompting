import hmac

# Example global dictionary of valid message signatures.
# In a real application this would be securely populated and stored.
VALID_API_MESSAGES = {
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # ... more message_id:signature pairs ...
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for the given message_id.

    Parameters
    ----------
    message_id : str
        The unique identifier of the message to be authenticated.
    signature : str
        The cryptographic signature associated with the message.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If message_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_signature = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, signature)