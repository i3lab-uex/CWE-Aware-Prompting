import hmac

# Example dictionary of message IDs mapped to their expected signatures.
# In a real system this would be securely stored and possibly rotated regularly.
VALID_API_MESSAGES = {
    "msg001": "3a7bd3e2360a4c6f9b1d5f2b8c8a7e3f",
    "msg002": "9f1c2d4b5a6e7f8g9h0i1j2k3l4m5n6o",
    # ... additional message ID → signature mappings ...
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        The identifier of the message to verify.
    sign : str
        The cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    KeyError
        If `msg_id` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use a constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(sign, expected_sign)