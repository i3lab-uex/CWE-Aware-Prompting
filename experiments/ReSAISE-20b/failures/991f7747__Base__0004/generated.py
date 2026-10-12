import hmac

# Global dictionary mapping message IDs to their expected cryptographic signatures.
# In a real-world scenario, this would be populated from secure storage or
# an external service and not hard-coded.
VALID_API_MESSAGES = {
    # Example entries (hex-encoded signatures)
    "msg1": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg2": "e99a18c428cb38d5f260853678922e03",
    # Add more message IDs and their expected signatures here.
}


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): Unique identifier of the API message.
        crypto_signature (str): Cryptographic signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `api_message_id` does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists
    if api_message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown API message ID: {api_message_id}")

    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_signature, crypto_signature)