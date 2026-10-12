import hmac

# Global dictionary mapping message IDs to their expected signatures.
# Example: {"msg123": "5f2d...", ...}
VALID_API_MESSAGES = {
    # Populate with actual expected signatures.
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        Unique identifier for the API message.
    crypto_signature : str
        Cryptographic signature to validate.

    Returns
    -------
    bool
        True if the signature is valid for the message ID, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in the VALID_API_MESSAGES dict.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)