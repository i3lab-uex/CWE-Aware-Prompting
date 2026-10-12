import hmac

# Global dictionary mapping message identifiers to their valid signatures.
# Example structure: {"msg1": "a1b2c3...", ...}
VALID_API_MESSAGES = {
    # Populate with real values in production
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    valid signature for a given message identifier.

    Args:
        msg_identifier: Identifier of the message to verify.
        sign: The cryptographic signature provided by the external API.

    Returns:
        True if the signature matches, False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError propagates if not found
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sign, expected_sign)