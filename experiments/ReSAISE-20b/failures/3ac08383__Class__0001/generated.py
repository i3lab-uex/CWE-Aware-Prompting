import hmac

# Global dictionary mapping API messages to their expected cryptographic signatures.
# In a real application, this would be populated from secure storage or configuration.
VALID_API_MESSAGES = {
    # Example entries (hex-encoded signatures)
    "msg1": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg2": "e99a18c428cb38d5f260853678922e03",
    # Add more message-signature pairs as needed.
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message.

    Parameters:
        api_message (str): Identifier of the API message.
        sig (str): Signature to validate against the stored value.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `api_message` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message exists; raise KeyError if missing
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sig, sig)