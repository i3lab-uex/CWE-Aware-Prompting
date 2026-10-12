import hmac

# Example global dictionary of valid signatures.
# In a real system, this would be populated securely from the API provider.
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "b1c2d3e4f5g6h7i8j9k0",
    # ... more entries ...
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        message_id (str): The unique identifier of the message.
        signature (str): The cryptographic signature supplied by the API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `message_id` is not present in VALID_API_MESSAGES.
    """
    if message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{message_id}' not found")

    expected_signature = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to avoid timing attacks (CWE-347)
    return hmac.compare_digest(signature, expected_signature)