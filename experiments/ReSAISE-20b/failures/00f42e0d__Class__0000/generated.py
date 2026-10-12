import hashlib
import hmac

# List of known weak or broken hash algorithms that should not be used for signing
_WEAK_HASHES = {
    'md5',
    'sha1',
    'md4',
    # Add any other known weak algorithms here if desired
}

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (case‑insensitive).
    message : bytes
        The message that needs to be signed.
    key : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the hash algorithm is not available or is considered weak.
    """
    if not isinstance(hash_name, str):
        raise TypeError("hash_name must be a string")

    # Normalise the hash name
    norm_hash = hash_name.lower()

    # Reject weak algorithms to avoid CWE‑327
    if norm_hash in _WEAK_HASHES:
        raise ValueError(f"Hash algorithm '{hash_name}' is considered weak and is not allowed for signing")

    # Check that the hash algorithm exists in hashlib
    if norm_hash not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available in hashlib")

    # Create a new HMAC object using the specified hash function
    try:
        digest = hmac.new(key, message, hashlib.new(norm_hash)).digest()
    except Exception as exc:
        # Wrap any unexpected exception into a ValueError for clarity
        raise ValueError(f"Failed to compute HMAC with algorithm '{hash_name}': {exc}") from exc

    return digest