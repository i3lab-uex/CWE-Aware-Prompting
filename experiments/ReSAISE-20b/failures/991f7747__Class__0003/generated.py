import hmac

# Global dictionary mapping message IDs to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries (should be replaced with real values in production)
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef",
    # Add more entries as needed
}


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters:
        api_message_id (str): The unique identifier of the API message.
        crypto_signature (str): The cryptographic signature to validate.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError propagates if not found
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use a timing‑safe comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)