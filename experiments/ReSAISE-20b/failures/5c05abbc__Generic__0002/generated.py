import hmac
from typing import Dict

# Global dictionary containing the correct signatures for each message ID.
# In a real application this would be populated from a secure source.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # ... more entries ...
}


def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        The identifier of the API message.
    sign : str
        The cryptographic signature supplied by the external source.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `msg_id` is not present in ``VALID_API_MESSAGES``.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected, sign)