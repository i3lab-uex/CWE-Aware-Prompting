import hmac

# Global dictionary containing the correct cryptographic signatures for API messages.
# Example structure: {"msg123": "signature1", "msg456": "signature2"}
VALID_API_MESSAGES = {
    # This dictionary should be populated with real values in production.
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Args:
        msg_id (str): The identifier of the API message.
        sign (str): The cryptographic signature to validate.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, sign)