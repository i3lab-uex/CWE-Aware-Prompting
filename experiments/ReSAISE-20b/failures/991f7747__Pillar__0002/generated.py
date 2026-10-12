import hmac

# Global dictionary containing expected cryptographic signatures for API messages.
# Example structure: {"msg1": "signature1", "msg2": "signature2"}
VALID_API_MESSAGES = {
    # Populate with real values in production
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): Unique identifier of the message.
        crypto_signature (str): Signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists
    if api_message_id not in VALID_API_MESSAGES:
        raise KeyError(f"API message ID '{api_message_id}' is not recognized.")

    # Retrieve the expected signature
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(crypto_signature, expected_signature)