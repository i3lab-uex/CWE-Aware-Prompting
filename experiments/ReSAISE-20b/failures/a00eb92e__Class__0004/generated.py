import hmac

# Predefined dictionary of valid message identifiers to their cryptographic signatures.
# In a real application this would be securely stored and possibly rotated periodically.
VALID_API_MESSAGES = {
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # ... more entries ...
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored value
    for the given message identifier.

    Parameters:
        msg_identifier (str): The ID of the message to verify.
        crypto_sign (str): The cryptographic signature supplied by the external API.

    Returns:
        bool: True if the signature matches the stored value; False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Ensure the message identifier exists
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{msg_identifier}' not found.")

    # Retrieve the expected signature
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)