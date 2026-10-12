import hmac

# Example global dictionary of valid message signatures.
# In a real application this would be securely stored and populated elsewhere.
VALID_API_MESSAGES = {
    "msg001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg002": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Parameters:
        msg_id (str): Identifier of the message.
        sign (str): Cryptographic signature to verify.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected, sign)