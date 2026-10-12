import hmac
from typing import Dict

# Example global dictionary of expected signatures.
# In a real application this would be securely populated and stored.
VALID_API_MESSAGES: Dict[str, str] = {
    # api_message_id : expected_signature
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # ... more entries ...
}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the supplied cryptographic signature `sig` matches the
    expected signature for the given `api_message`.

    Parameters
    ----------
    api_message : str
        Identifier of the message whose signature is to be verified.
    sig : str
        Cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `api_message` is not present in the global VALID_API_MESSAGES dict.
    """
    # Ensure that the message exists; otherwise raise KeyError
    if api_message not in VALID_API_MESSAGES:
        raise KeyError(f"API message '{api_message}' not found")

    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sig, expected_sig)