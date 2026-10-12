import hmac

# Example dictionary of valid signatures for API messages.
# In a real system this would be securely populated from a trusted source.
VALID_API_MESSAGES = {
    # 'msg_identifier': 'hex_encoded_signature'
    "order_123": "a3f1c4d2e9b7...",
    # Add more entries as needed
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    valid signature for a given message identifier.

    Args:
        msg_identifier (str): The identifier of the API message.
        sign (str): The cryptographic signature to verify.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to avoid timing attacks
    return hmac.compare_digest(sign, expected_sign)