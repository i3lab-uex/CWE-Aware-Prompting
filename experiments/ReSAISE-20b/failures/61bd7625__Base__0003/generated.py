import hmac

# Global dictionary mapping message IDs to their expected signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with real values)
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # ...
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected cryptographic
    signature for `message_id`.

    Parameters:
        message_id (str): The unique identifier of the message.
        signature   (str): The cryptographic signature supplied by the API.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If `message_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists
    expected_signature = VALID_API_MESSAGES[message_id]  # may raise KeyError

    # Perform a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(signature, expected_signature)