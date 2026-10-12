import hmac

# Example global dictionary of valid API messages and their expected signatures.
# In practice, this would be securely loaded from a trusted source or configuration file.
VALID_API_MESSAGES = {
    "msg-001": "a3f5c8e2d4b7...",
    "msg-002": "9b1f0a6c3e8d...",
    # ... more entries ...
}


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): The unique identifier of the API message.
        crypto_signature (str): The cryptographic signature to validate.

    Returns:
        bool: True if the signature is valid for the message ID, False otherwise.

    Raises:
        KeyError: If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not.
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(crypto_signature, expected_signature)