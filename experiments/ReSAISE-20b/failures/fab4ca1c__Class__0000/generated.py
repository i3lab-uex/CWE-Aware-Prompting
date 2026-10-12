import hmac

# Global dictionary mapping message identifiers to their valid signatures.
# In a real application, this would be securely stored and managed.
VALID_API_MESSAGES = {
    # Example entries (signature strings should be hex-encoded or base64 as appropriate)
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed
}


def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Args:
        msg_identifier: Identifier of the message to validate.
        sign: Cryptographic signature received from the API.

    Returns:
        True if the signature matches the stored value; False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sign)