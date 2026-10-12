import hmac

# Global dictionary mapping message IDs to their expected cryptographic signatures.
# Example (hex-encoded SHA256 HMACs). In a real system these would be securely stored.
VALID_API_MESSAGES = {
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # Add more message-signature pairs as needed
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature `sig` matches the
    expected signature for the given `api_message`.

    Parameters:
        api_message (str): Identifier of the message to verify.
        sig (str): Cryptographic signature supplied by the external API.

    Returns:
        bool: True if the signature is valid for the given message, False otherwise.

    Raises:
        KeyError: If `api_message` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message exists; raise KeyError if it does not
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use hmac.compare_digest for constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sig, expected_sig)