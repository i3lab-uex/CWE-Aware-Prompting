import hmac

# Example global dictionary of valid signatures for each message ID.
# In production, this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    # msg_id: signature
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "abcdef1234567890",
    # ... add more entries as needed ...
}


def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the authenticity of a message received from an external API.

    Parameters
    ----------
    msg_id : str
        Identifier for the message whose authenticity needs to be checked.
    sig : str
        Cryptographic signature associated with the specified message.

    Returns
    -------
    bool
        True if the provided signature matches the stored one for the given msg_id,
        otherwise False.

    Raises
    ------
    KeyError
        If the msg_id does not exist in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is unknown
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, sig)