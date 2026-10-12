import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
# Example (replace with actual data):
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # ... add more entries as needed
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Args:
        msg_code (str): Identifier of the message to validate.
        crypto_sign (str): Cryptographic signature supplied by the API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_code` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message code exists
    if msg_code not in VALID_API_MESSAGES:
        raise KeyError(f"Message code '{msg_code}' is unknown.")

    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use hmac.compare_digest for a timing‑attack resistant comparison.
    # Convert both signatures to bytes; if they are already hex strings, we keep them as is.
    # If the signatures may be binary data, adjust accordingly.
    return hmac.compare_digest(expected_sign.encode(), crypto_sign.encode())