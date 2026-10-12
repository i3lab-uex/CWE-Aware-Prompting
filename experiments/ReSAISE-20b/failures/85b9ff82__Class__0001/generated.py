import hashlib
import hmac

# Global secret key used for HMAC. In a real application this should be
# securely generated and stored, not hard‑coded.
secret_key: bytes = b"super_secret_key"

# Set of hash algorithms considered secure for HMAC usage.
SECURE_HASH_ALGORITHMS = {
    "sha224",
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

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Create an HMAC signature of `content` using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    content : bytes
        Raw data to sign.

    Returns
    -------
    bytes
        The HMAC signature.

    Raises
    ------
    ValueError
        If `hash_algorithm` is not supported or is disallowed.
    """
    # Normalise the algorithm name (case‑insensitive)
    algo_name = hash_algorithm.lower()

    # Ensure the requested algorithm is in our whitelist of secure algorithms
    if algo_name not in SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {hash_algorithm}")

    # Instantiate the hash function
    try:
        hash_func = hashlib.new(algo_name)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm {hash_algorithm} is not available") from exc

    # Compute HMAC
    return hmac.new(secret_key, content, digestmod=hash_func).digest()