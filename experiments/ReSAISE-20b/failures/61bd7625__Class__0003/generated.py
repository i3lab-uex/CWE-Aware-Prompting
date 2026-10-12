import hmac
import hashlib

# Global dictionary mapping message IDs to their expected signatures.
# Example: VALID_API_MESSAGES = {"msg1": "abc123...", "msg2": "def456..."}
VALID_API_MESSAGES = {}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        message_id (str): The unique identifier of the message.
        signature (str): The cryptographic signature to verify.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If the message_id is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sig.encode(), signature.encode())