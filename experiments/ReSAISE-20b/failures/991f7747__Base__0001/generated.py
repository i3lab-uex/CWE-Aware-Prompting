import hmac

# Global dictionary mapping message IDs to expected signatures.
# In a real application this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    # Example entries; replace with actual values
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for the given API message ID.

    Parameters:
        api_message_id (str): Unique identifier of the API message.
        crypto_signature (str): Signature to be validated.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    if api_message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown API message ID: {api_message_id}")

    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_signature, crypto_signature)