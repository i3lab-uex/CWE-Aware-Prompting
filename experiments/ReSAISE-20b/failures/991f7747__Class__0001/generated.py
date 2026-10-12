import hmac

# Global dictionary containing the expected cryptographic signatures for each API message.
# In a real-world scenario this would be populated from a secure source.
VALID_API_MESSAGES = {
    # Example entries (message_id: expected_signature)
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed.
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): Unique identifier of the API message.
        crypto_signature (str): Signature to be validated.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to avoid timing attacks
    return hmac.compare_digest(crypto_signature, expected_signature)