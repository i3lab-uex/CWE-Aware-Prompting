import hmac

# Global dictionary mapping API message identifiers to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with real values)
    "msg_123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_456": "e99a18c428cb38d5f260853678922e03",
    # Add more messages and signatures as needed
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature `sig` matches
    the expected signature for the given `api_message`.

    Parameters:
        api_message (str): Identifier of the API message.
        sig (str): Cryptographic signature to validate.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If `api_message` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError will propagate if not found
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)