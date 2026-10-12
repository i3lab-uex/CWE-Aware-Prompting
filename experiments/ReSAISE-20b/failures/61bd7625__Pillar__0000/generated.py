import hmac
import hashlib

# Global dictionary mapping message IDs to their expected signatures.
# Example format: {'msg123': 'a1b2c3...', ...}
VALID_API_MESSAGES = {
    # Populate with actual expected signatures here
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected
    cryptographic signature for the given `message_id`.

    Args:
        message_id (str): Unique identifier of the message.
        signature (str): Cryptographic signature supplied by the API.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError propagates if not found
    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(signature, expected_sig)