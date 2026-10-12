import hmac

# Global dictionary mapping message IDs to their expected signatures.
# Example structure: {"msg123": "hex_signature_string", ...}
VALID_API_MESSAGES = {
    # Populate with actual message IDs and signatures as needed.
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        msg_id (str): Identifier of the message.
        sig (str): Cryptographic signature supplied by the API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `msg_id` does not exist in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)