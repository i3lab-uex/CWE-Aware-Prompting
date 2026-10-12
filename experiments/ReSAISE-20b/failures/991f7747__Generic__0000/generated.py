import hmac

# Global dictionary mapping message IDs to their expected signatures.
# Example:
# VALID_API_MESSAGES = {
#     "msg123": "a1b2c3d4e5f6g7h8i9j0",
#     "msg456": "1234567890abcdef"
# }
VALID_API_MESSAGES = {}  # Should be populated elsewhere in the application


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters:
        api_message_id (str): The unique identifier of the message.
        crypto_signature (str): The signature to validate.

    Returns:
        bool: True if the signature matches the stored one, False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists
    if api_message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{api_message_id}' not found in VALID_API_MESSAGES")

    # Retrieve the expected signature
    expected_sig = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, crypto_signature)