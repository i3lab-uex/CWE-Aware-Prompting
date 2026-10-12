import hmac

# Global dictionary mapping message IDs to their expected signatures.
# Example:
# VALID_API_MESSAGES = {
#     "msg-001": "a1b2c3d4e5f6...",
#     "msg-002": "deadbeef1234..."
# }
VALID_API_MESSAGES = {}  # The real values should be provided elsewhere.

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for the given message ID.

    Parameters:
        message_id (str): Unique identifier of the API message.
        signature  (str): Cryptographic signature supplied by the caller.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists
    if message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{message_id}' not found.")

    expected_sig = VALID_API_MESSAGES[message_id]

    # Constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, signature)