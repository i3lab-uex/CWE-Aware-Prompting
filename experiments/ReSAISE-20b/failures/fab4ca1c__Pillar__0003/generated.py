import hmac

# Global dictionary containing valid signatures for each message identifier.
# Example: VALID_API_MESSAGES = {"msg1": "5f4dcc3b5aa765d61d8327deb882cf99", ...}
VALID_API_MESSAGES = {}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Args:
        msg_identifier: Identifier of the message to validate.
        sign: Cryptographic signature provided by the external API.

    Returns:
        True if the signature is valid for the given identifier, False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Ensure the identifier exists; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to prevent timing attacks (CWE-693).
    return hmac.compare_digest(sign, expected_sign)