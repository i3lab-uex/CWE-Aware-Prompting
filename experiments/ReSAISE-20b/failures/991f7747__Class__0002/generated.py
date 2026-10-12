import hmac

# Global dictionary containing the expected cryptographic signatures for API messages.
# In a real application this would be populated from a secure source (e.g., environment variables, vault, etc.).
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
    # ... add more entries as needed ...
}


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected signature
    for a given API message ID.

    Args:
        api_message_id (str): Unique identifier of the API message.
        crypto_signature (str): Signature to validate.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If `api_message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if ID is missing
    try:
        expected_signature = VALID_API_MESSAGES[api_message_id]
    except KeyError as exc:
        raise KeyError(f"API message ID '{api_message_id}' not found.") from exc

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)