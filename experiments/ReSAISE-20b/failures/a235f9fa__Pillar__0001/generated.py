import hmac

# Global dictionary mapping message IDs to their expected cryptographic signatures.
# In a real application, this would be securely loaded from a trusted source.
VALID_API_MESSAGES = {
    # Example entries (signature strings are placeholders)
    "msg-001": "a3f5c9e2d1b4f6a7",
    "msg-002": "b8c9e3d1a2f4b7c6",
    # Add more message IDs and their corresponding signatures here.
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature of a message received from an external API.

    Args:
        msg_id (str): Identifier for the message.
        sig (str): Cryptographic signature provided with the message.

    Returns:
        bool: True if the signature matches the expected value for msg_id, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is unknown
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(sig, expected_sig)