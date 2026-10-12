import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
# In a real application, this would be securely loaded from a protected source.
VALID_API_MESSAGES = {
    # Example entries (hashes should be generated using the same algorithm as the API)
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef0123",
    # Add more entries as needed
}


def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for the given message identifier.

    Parameters:
        msg_identifier (str): Identifier of the API message.
        sign (str): Cryptographic signature received from the external API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `msg_identifier` does not exist in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature for the given message identifier.
    expected_sign = VALID_API_MESSAGES[msg_identifier]  # May raise KeyError

    # Use constant-time comparison to mitigate timing attacks (CWE-693).
    return hmac.compare_digest(expected_sign, sign)