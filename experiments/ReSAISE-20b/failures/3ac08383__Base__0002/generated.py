import hmac

# Global dictionary mapping API message identifiers to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with actual values)
    "msg-123": "a1b2c3d4e5f6g7h8i9j0",
    "msg-456": "1234567890abcdef1234",
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message.

    Parameters:
        api_message (str): Identifier of the API message.
        sig (str): Cryptographic signature to verify.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `api_message` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message exists; raise KeyError if it does not
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(sig, expected_sig)