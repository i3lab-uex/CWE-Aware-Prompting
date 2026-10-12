import hmac
import hashlib

# Global dictionary containing the expected HMAC‑SHA256 signatures for each API message.
# Example entry: {"msg1": "a3f5c9..."}  # hex string of the HMAC digest
VALID_API_MESSAGES = {
    # Populate with actual message:signature pairs in real usage.
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message.

    Parameters
    ----------
    api_message : str
        The unique identifier of the message whose signature is to be verified.
    sig : str
        The cryptographic signature (hexadecimal string) supplied by the external API.

    Returns
    -------
    bool
        True if the signature is valid for the given message, False otherwise.

    Raises
    ------
    KeyError
        If `api_message` is not present in the global VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected_sig = VALID_API_MESSAGES[api_message]

    # Perform a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sig.lower(), sig.lower())