# Global dictionary mapping API message identifiers to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries – replace with real data as needed
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "0123456789abcdef1234",
    # Add more message-signature pairs here
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message.

    Parameters
    ----------
    api_message : str
        The unique identifier of the message to verify.
    sig : str
        The cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    KeyError
        If `api_message` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature for the given message
    try:
        expected_sig = VALID_API_MESSAGES[api_message]
    except KeyError as exc:
        # Re‑raise with a clear message
        raise KeyError(f"Unknown API message identifier: {api_message}") from exc

    # Constant‑time comparison to mitigate timing attacks
    return _constant_time_compare(sig, expected_sig)

def _constant_time_compare(a: str, b: str) -> bool:
    """
    Perform a constant‑time comparison of two strings.

    Parameters
    ----------
    a, b : str
        Strings to compare.

    Returns
    -------
    bool
        True if the strings are identical, False otherwise.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode('utf-8'), b.encode('utf-8')):
        result |= x ^ y
    return result == 0