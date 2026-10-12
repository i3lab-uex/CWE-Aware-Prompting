import hmac

# Global dictionary mapping message IDs to their expected cryptographic signatures.
# In a real system this would be populated from a secure source or configuration.
VALID_API_MESSAGES = {
    # Example entries:
    # "msg123": "5f4dcc3b5aa765d61d8327deb882cf99",
    # "msg456": "e99a18c428cb38d5f260853678922e03",
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        msg_id (str): The identifier of the message to verify.
        sign (str): The cryptographic signature supplied by the API.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature. This will raise KeyError if msg_id is missing,
    # which signals that the message is unrecognized.
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use hmac.compare_digest for a timing‑attack resistant comparison.
    return hmac.compare_digest(sign, expected_sign)