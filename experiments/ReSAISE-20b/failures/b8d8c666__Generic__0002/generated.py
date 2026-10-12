import hashlib
import hmac

# Global secret key used for HMAC signing (example placeholder)
secret_key: bytes = b"super_secret_key"

# Define a set of secure hash algorithms that are allowed.
# These exclude weak or legacy algorithms such as MD5, SHA1, RIPEMD160, etc.
ALLOWED_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature of the given payload using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the algorithm is unsupported or disallowed.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algorithm_name}")

    # Retrieve the constructor from hashlib
    try:
        hash_func = getattr(hashlib, algo)
    except AttributeError:
        # This should not happen if ALLOWED_ALGORITHMS is accurate,
        # but we guard against it just in case.
        raise ValueError(f"Hash algorithm not available: {algorithm_name}")

    # Create an HMAC object with the chosen hash function
    h = hmac.new(secret_key, msg=payload, digestmod=hash_func)
    return h.digest()