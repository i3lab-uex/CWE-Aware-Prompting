import hmac

# Example global dictionary of valid signatures for messages.
# In production, this would be populated securely (e.g., from a database or environment).
VALID_API_MESSAGES = {
    # msg_id: signature
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Parameters:
        msg_id (str): The unique identifier of the API message.
        sign   (str): The cryptographic signature received with the message.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure msg_id exists
    if msg_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{msg_id}' not found in VALID_API_MESSAGES")

    # Retrieve the expected signature
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, sign)