import hmac

# Global dictionary mapping message IDs to their valid signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with real data in production)
    "msg123": "a1b2c3d4e5f6g7h8i9j0",
    "msg456": "1a2b3c4d5e6f7g8h9i0j",
    # Add more message ID → signature pairs as needed
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the
    expected signature for a given message ID.

    Parameters:
        msg_id (str): Identifier of the message to validate.
        sig (str): Signature supplied by the external API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists
    if msg_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{msg_id}' is unknown.")

    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)