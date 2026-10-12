import hmac

# Global dictionary containing valid signatures for API messages.
# Example format: {"msg1": "hexsignature...", ...}
VALID_API_MESSAGES = {
    # Populate with actual message IDs and their expected signatures.
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the authenticity of a message by comparing its provided signature
    against the expected signature stored in VALID_API_MESSAGES.

    Args:
        msg_id (str): Identifier of the message to validate.
        sig (str): Cryptographic signature received from the external API.

    Returns:
        bool: True if the signature matches the expected value, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found.
    expected_sig = VALID_API_MESSAGES[msg_id]  # May raise KeyError

    # Perform a constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(expected_sig, sig)