import hmac

# Example dictionary of valid signatures for demonstration purposes.
# In a real system, this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg-001": "5f2c3a1e8b9d4a7f0c6e2d5b9a3e1f0d",
    "msg-002": "8b7c4e9a2f1d3c6b0e5d7f8a9c2b4d6",
    # Add more message IDs and their expected signatures here
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters:
        api_message_id (str): Unique identifier of the message.
        crypto_signature (str): Signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; otherwise raise KeyError
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)