import hmac

# Global dictionary mapping message IDs to their expected signatures.
# Example entries (replace with actual values in production).
VALID_API_MESSAGES = {
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # Add more message_id: signature pairs as needed.
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        message_id (str): The unique identifier of the message.
        signature   (str): The cryptographic signature received from the API.

    Returns:
        bool: True if the signature matches the expected value, False otherwise.

    Raises:
        KeyError: If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; otherwise raise KeyError
    if message_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{message_id}' not found.")

    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(signature, expected_sig)