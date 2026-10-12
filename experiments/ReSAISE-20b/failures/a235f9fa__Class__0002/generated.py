import hmac

# Global dictionary mapping message IDs to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with real values in production)
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "6cb75f2c3d9b4e1a8e5e7c2f3a9b4d6e",
    # ... add more entries as needed
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        msg_id (str): Identifier of the message to validate.
        sig (str): Cryptographic signature supplied by the external API.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is unknown
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)