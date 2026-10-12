import hmac

# Global dictionary mapping API message IDs to their expected cryptographic signatures.
# In a real application this would be populated from secure storage or an external source.
VALID_API_MESSAGES = {
    "msg-001": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "msg-002": "a5d9e7f9c1f4b8e6d3a2c7f5b0e4d9c1f7a8b6c3d2e1f9a0b4c5d6e7f8g9h0i",
    # Add more message IDs and their expected signatures here.
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters:
        api_message_id (str): Unique identifier of the API message.
        crypto_signature (str): Cryptographic signature to validate.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)