import hmac

# Global dictionary mapping API message IDs to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with actual values in production)
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # Add more message IDs and signatures as needed
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        Unique identifier of the API message to validate.
    crypto_signature : str
        The cryptographic signature supplied by the external source.

    Returns
    -------
    bool
        True if the signature is valid for the given message ID, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)