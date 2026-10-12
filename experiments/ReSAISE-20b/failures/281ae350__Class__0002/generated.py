import secrets

# Example global dictionary of expected signatures.
# In real usage, this would be securely populated and protected.
VALID_API_MESSAGES = {
    # msg_identifier: expected_signature
    "msg1": "5f2c9e7a1d3b4f8e6a9c0b2d1f5e7a3c",
    "msg2": "9a4b8d6f1e2c3a7b0f5d4e9c8b6a2d1",
    # Add more entries as needed.
}


def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Args:
        msg_identifier: Unique identifier of the API message.
        crypto_signature: Signature supplied with the message.

    Returns:
        True if the signature is valid, False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature. Let KeyError propagate if not found.
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to avoid timing attacks.
    return secrets.compare_digest(expected_signature, crypto_signature)