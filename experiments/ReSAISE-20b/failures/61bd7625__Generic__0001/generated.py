import hmac

# Global dictionary mapping message IDs to their expected signatures.
# In real usage this would be populated with the actual data from your system.
VALID_API_MESSAGES = {
    # Example:
    # "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected signature for
    `message_id` stored in VALID_API_MESSAGES.

    Args:
        message_id (str): The unique identifier of the message.
        signature (str): The cryptographic signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if message_id is missing
    expected_sig = VALID_API_MESSAGES[message_id]

    # Use hmac.compare_digest for constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(signature, expected_sig)