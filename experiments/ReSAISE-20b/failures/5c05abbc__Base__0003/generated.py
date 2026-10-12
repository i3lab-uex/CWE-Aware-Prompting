import hmac

# Example global dictionary containing valid signatures for API messages.
# In real usage this should be populated from a secure source.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f67890abcdef1234567890",
    "msg_002": "b2c3d4e5f67890abcdef1234567890a1",
    # Add more message IDs and their corresponding signatures here.
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for the given message ID.

    Parameters:
        msg_id (str): The ID of the message to verify.
        sign (str): The cryptographic signature received from the API.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If msg_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature for the message ID.
    try:
        expected_sign = VALID_API_MESSAGES[msg_id]
    except KeyError as exc:
        # Re-raise with a clear message while preserving the original exception context.
        raise KeyError(f"Message ID '{msg_id}' not found in VALID_API_MESSAGES") from exc

    # Use constant-time comparison to prevent timing attacks.
    return hmac.compare_digest(sign, expected_sign)