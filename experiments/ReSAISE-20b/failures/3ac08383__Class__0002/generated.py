import hmac
from typing import Dict

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
# In a real application this would be populated securely and never exposed publicly.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries (message_id : signature)
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "6c569aabbf7775ef8fc570e228c16b98",
    # ... more entries
}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message identifier.

    Parameters
    ----------
    api_message : str
        Unique identifier for the external API message.
    sig : str
        Cryptographic signature supplied by the external source.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    KeyError
        If `api_message` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve expected signature; raise KeyError if message not known
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)