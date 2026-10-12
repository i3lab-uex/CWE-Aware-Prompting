import secrets

# Global dictionary mapping message IDs to their expected cryptographic signatures.
# This should be populated elsewhere in the application.
VALID_API_MESSAGES = {
    # Example entries (these would normally be filled with real data)
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef",
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected cryptographic signature
    for the given `message_id`.

    Parameters:
        message_id (str): The unique identifier of the message to authenticate.
        signature (str): The cryptographic signature provided by the external API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return secrets.compare_digest(signature, expected_signature)