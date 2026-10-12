import hashlib
import hmac

# A secret key that must be kept confidential. In a real application this should
# come from a secure source (e.g., environment variable, key vault, etc.).
SECRET_KEY: bytes = b"your-very-secret-key"

# Whitelist of secure hash algorithms that are safe for HMAC usage.
SECURE_ALGORITHMS = {
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
    "sha3_256": hashlib.sha3_256,
    "sha3_384": hashlib.sha3_384,
    "sha3_512": hashlib.sha3_512,
    "blake2b": hashlib.blake2b,
    "blake2s": hashlib.blake2s,
}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using a secure hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The name of the desired hash algorithm (case-insensitive).
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the content.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    if not isinstance(content, (bytes, bytearray)):
        raise TypeError("content must be bytes-like")

    algo_key = hash_algorithm.lower()
    if algo_key not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {hash_algorithm!r}. "
            f"Supported algorithms are: {', '.join(SECURE_ALGORITHMS.keys())}"
        )

    hash_func = SECURE_ALGORITHMS[algo_key]
    hmac_obj = hmac.new(SECRET_KEY, content, hash_func)
    return hmac_obj.digest()