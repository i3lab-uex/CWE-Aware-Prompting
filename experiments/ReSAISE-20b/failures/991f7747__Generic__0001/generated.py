import hmac

# Example global dictionary mapping message IDs to their expected signatures.
# In a real application this would be securely stored and populated elsewhere.
VALID_API_MESSAGES = {
    "msg-001": "a3f5c2b1d4e6f7a8b9c0",
    "msg-002": "1d2e3f4a5b6c7d8e9f0a",
    # Add more entries as needed
}


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters:
        api_message_id (str): Unique identifier of the message.
        crypto_signature (str): The signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If api_message_id does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)