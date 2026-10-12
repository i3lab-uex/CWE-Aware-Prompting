import hashlib
import hmac

# Global secret key used for HMAC signing. In a real application this should be
# securely generated, stored and rotated.
secret_key: bytes = b'super_secret_hmac_key'

# List of hash algorithms considered secure for HMAC.
SECURE_HASH_ALGORITHMS = {
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
    'sha512_224',
    'sha512_256',
}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for `content` using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalize name to lowercase for comparison
    algo = hash_algorithm.lower()

    if algo not in SECURE_HASH_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: '{hash_algorithm}'. "
            "Supported secure algorithms are: "
            f"{', '.join(sorted(SECURE_HASH_ALGORITHMS))}"
        )

    # Verify that hashlib supports the algorithm (Python 3.6+ includes all listed)
    try:
        digestmod = hashlib.new(algo)
    except ValueError as exc:
        raise ValueError(
            f"Hash algorithm '{hash_algorithm}' is not available in this Python "
            "installation."
        ) from exc

    # Compute HMAC
    hmac_obj = hmac.new(secret_key, content, digestmod=hashlib.sha256)
    # Use the requested algorithm by reinitializing with correct digestmod
    hmac_obj = hmac.new(secret_key, content, digestmod=hashlib.new(algo))
    return hmac_obj.digest()