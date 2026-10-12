import hmac

# Example dictionary of valid signatures (hex strings) for each message ID.
# In a real application, this would be securely stored and possibly rotated.
VALID_API_MESSAGES = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "b2c3d4e5f6g7h8i9j0a1",
    # Add more entries as needed.
}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given API message.

    Parameters
    ----------
    api_message : str
        The unique identifier of the API message being validated.
    sig : str
        The cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if `sig` matches the stored signature for `api_message`,
        False otherwise.

    Raises
    ------
    KeyError
        If `api_message` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the message exists; raise KeyError if not.
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use hmac.compare_digest for a timing‑safe comparison.
    return hmac.compare_digest(sig, expected_sig)