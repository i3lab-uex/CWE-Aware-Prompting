import hmac

# Global dictionary containing valid signatures for each message ID.
# Example: {"msg123": "a1b2c3d4..."}
VALID_API_MESSAGES = {
    # Populate with real data in production
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the
    expected signature for a given message ID.

    Parameters:
        msg_id (str): Identifier of the message to validate.
        sig (str): Cryptographic signature received from the API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If msg_id does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists
    expected_sig = VALID_API_MESSAGES[msg_id]  # May raise KeyError

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, sig)