import hashlib
import hmac

# Global secret key used for HMAC signing.
# In a real application this should be stored securely (e.g., environment variable,
# key management service, or hardware security module) and never hard‑coded.
secret_key: bytes = b"super_secret_key_used_for_hmac_signing"

# A set of cryptographic hash algorithms considered secure for HMAC.
_SECURE_HASHES = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def _get_hashlib_func(name: str):
    """
    Return a hashlib constructor for the given algorithm name.
    Raises ValueError if the algorithm is not supported or insecure.
    """
    name = name.lower()
    if name not in _SECURE_HASHES:
        raise ValueError(f"Unsupported or insecure hash algorithm: {name!r}")
    # hashlib.new accepts the algorithm name directly.
    return lambda: hashlib.new(name)

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given data.

    Parameters
    ----------
    hash_algorithm : str
        The name of a secure hash algorithm (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the content using the specified hash algorithm.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    if not isinstance(content, bytes):
        raise TypeError("content must be of type 'bytes'")

    # Retrieve the hashlib constructor for the chosen algorithm.
    digest_factory = _get_hashlib_func(hash_algorithm)

    # Compute HMAC using the global secret key and the chosen hash function.
    h = hmac.new(secret_key, content, digestmod=digest_factory)
    return h.digest()