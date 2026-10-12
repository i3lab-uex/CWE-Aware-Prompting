import hmac

# Global dictionary mapping API message IDs to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with real values)
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "0j9i8h7g6f5e4d3c2b1a",
    # Add more entries as needed
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): The unique identifier of the API message.
        crypto_signature (str): The signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)