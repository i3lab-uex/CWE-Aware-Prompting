import hashlib
import hmac

# Secret key used for HMAC. In practice, this should be securely stored and loaded.
secret_key: bytes = b"your-very-secure-secret-key"

# Define the set of hash algorithms that are considered secure for this context.
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

# Ensure the algorithms are actually available in this Python build.
AVAILABLE_ALGORITHMS = set(hashlib.algorithms_available)
ALLOWED_ALGORITHMS = SECURE_HASH_ALGORITHMS & AVAILABLE_ALGORITHMS

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Create an HMAC signature of the given content using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    content : bytes
        Raw input data to be signed.

    Returns
    -------
    bytes
        The HMAC signature computed from the content.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or disallowed.
    """
    # Normalise the algorithm name to lower case
    algo = hash_algorithm.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: '{hash_algorithm}'. "
            f"Allowed algorithms are: {sorted(ALLOWED_ALGORITHMS)}"
        )

    # Retrieve the actual hash constructor from hashlib
    try:
        digestmod = getattr(hashlib, algo)
    except AttributeError as exc:
        raise ValueError(
            f"Hash algorithm '{hash_algorithm}' is not available in this environment."
        ) from exc

    # Compute HMAC
    return hmac.new(secret_key, content, digestmod=digestmod).digest()