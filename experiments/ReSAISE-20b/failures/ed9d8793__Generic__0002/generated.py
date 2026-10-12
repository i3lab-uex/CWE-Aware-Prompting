import hashlib
import hmac

# The secret key used for HMAC signing (should be kept secure and not hard‑coded in production)
secret_key: bytes = b"YOUR_SECURE_SECRET_KEY"

# Whitelist of secure hash algorithms
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",
    "sha3_224",
    "shake_128",  # note: variable output length; use only if needed
    "sha512",
    "sha512_224",
    "shake_256",  # variable output length
    "sha3_512",
    "blake2s",
    "sha3_384",
}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    content : bytes
        Data to be signed.

    Returns
    -------
    bytes
        HMAC digest of the content.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name
    algo = hash_algorithm.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    # Verify that the algorithm is actually available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {hash_algorithm} is not available on this platform")

    # Create HMAC object and return the digest
    h = hmac.new(secret_key, content, getattr(hashlib, algo))
    return h.digest()