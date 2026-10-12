import hashlib
import hmac

# A set of hash algorithms considered secure for HMAC usage.
_SECURE_HASHES = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_224",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

# The secret key used for HMAC signing.
# In a real application this should be securely generated and stored.
_secret_key = b"your-very-secure-secret-key"

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the content.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    # Normalize algorithm name
    algo = hash_algorithm.lower()
    if algo not in _SECURE_HASHES:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    # Create a new hash object for the chosen algorithm
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm {hash_algorithm} is not available") from exc

    # Compute HMAC using the secret key
    hmac_obj = hmac.new(_secret_key, content, hasher)
    return hmac_obj.digest()