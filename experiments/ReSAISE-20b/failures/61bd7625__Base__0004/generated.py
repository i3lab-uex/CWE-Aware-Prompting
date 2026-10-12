import hmac

# Global dictionary mapping message IDs to their expected signatures.
# In a real application this would be securely loaded from configuration or
# a trusted source. For the purpose of this example it is defined here.
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "abcdef1234567890abcd",
    # Add more message IDs and their expected signatures here.
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters
    ----------
    message_id : str
        The unique identifier of the message to be authenticated.
    signature : str
        The cryptographic signature provided by the external API.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If ``message_id`` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to prevent timing attacks
    return hmac.compare_digest(signature, expected_signature)