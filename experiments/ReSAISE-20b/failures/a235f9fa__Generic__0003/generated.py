import hmac

# Example global dictionary mapping message IDs to their valid signatures.
# In real usage, this should be populated securely and kept confidential.
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # ... other entries ...
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature of a message received from an external API.

    Parameters
    ----------
    msg_id : str
        The identifier of the message whose authenticity needs to be checked.
    sig : str
        The cryptographic signature provided for the message.

    Returns
    -------
    bool
        True if `sig` matches the stored signature for `msg_id`, False otherwise.

    Raises
    ------
    KeyError
        If the provided `msg_id` does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; otherwise, raise KeyError
    if msg_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{msg_id}' not found in VALID_API_MESSAGES")

    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(sig, expected_sig)