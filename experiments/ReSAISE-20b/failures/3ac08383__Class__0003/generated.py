import hmac
import hashlib

# Global dictionary mapping API message identifiers to their expected HMAC signatures.
# In a real system these would be generated using a shared secret key.
VALID_API_MESSAGES = {
    # Example entries (message_id: expected_hmac_hex)
    "msg_001": "d2c7f6b5a8e3b4e9c1f2a0d4f7b6c5e8f3a9b2c1d4e6f7a8b0c1d2e3f4a5b6c7",
    "msg_002": "a1b2c3d4e5f60718293a4b5c6d7e8f9a0b1c2d3e4f506172839405060708090",
    # ... add more messages as needed
}

# Shared secret key used for HMAC generation/verification.
# In practice this should be stored securely (e.g., in a key management service).
_SHARED_SECRET_KEY = b"super_secret_shared_key"


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature `sig` matches the
    expected HMAC-SHA256 signature for the given `api_message`.

    Parameters
    ----------
    api_message : str
        Identifier of the API message to verify.
    sig : str
        Hex-encoded HMAC signature supplied with the message.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `api_message` is not present in VALID_API_MESSAGES.
    """
    if api_message not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown API message: {api_message}")

    expected_sig = VALID_API_MESSAGES[api_message]

    # Convert both signatures to bytes for constant‑time comparison.
    try:
        sig_bytes = bytes.fromhex(sig)
        expected_bytes = bytes.fromhex(expected_sig)
    except ValueError:
        # If the provided signature is not valid hex, treat it as invalid.
        return False

    # Use hmac.compare_digest to avoid timing attacks (CWE-345 mitigation).
    return hmac.compare_digest(sig_bytes, expected_bytes)