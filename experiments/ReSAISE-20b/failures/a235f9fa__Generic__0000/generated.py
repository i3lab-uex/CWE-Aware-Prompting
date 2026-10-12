import hmac

# Example global dictionary containing valid signatures for API messages.
# In a real application this would be securely loaded from a trusted source.
VALID_API_MESSAGES = {
    # msg_id: signature
    "msg001": "a1b2c3d4e5f6g7h8i9j0",
    "msg002": "1234567890abcdef1234",
    # Add more entries as needed
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature of a message received from an external API.

    Parameters
    ----------
    msg_id : str
        Identifier for the message to be validated.
    sig : str
        Cryptographic signature provided by the API.

    Returns
    -------
    bool
        True if the signature matches the expected value for the given msg_id,
        False otherwise.

    Raises
    ------
    KeyError
        If the provided msg_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is unknown
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)