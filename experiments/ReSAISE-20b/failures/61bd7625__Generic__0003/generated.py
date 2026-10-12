import hmac

# Global dictionary containing expected signatures for API messages.
VALID_API_MESSAGES = {
    # Example entries; in practice these would be populated elsewhere
    "msg_001": "a3f5c1e9d4b2f8a7",
    "msg_002": "b6c1e3d9f0a2b4c8",
    # ...
}


def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message_id.

    Parameters:
        message_id (str): Unique identifier of the API message.
        signature (str): Cryptographic signature supplied by the API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If message_id does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message_id exists
    if message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{message_id}' not found.")

    expected_sig = VALID_API_MESSAGES[message_id]

    # Use hmac.compare_digest for a timing‑safe comparison
    return hmac.compare_digest(signature, expected_sig)