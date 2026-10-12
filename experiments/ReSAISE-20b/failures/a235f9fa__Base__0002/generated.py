import hmac

# Global dictionary containing valid signatures for API messages.
# Example structure: {"msg123": "base64encodedSignature", ...}
VALID_API_MESSAGES = {
    # Populate with real message IDs and signatures as needed.
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Args:
        msg_id: Identifier of the message to validate.
        sig:   Signature provided by the external API.

    Returns:
        True if the signature matches the expected value, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is unknown.
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant-time comparison to mitigate timing attacks.
    return hmac.compare_digest(sig, expected_sig)