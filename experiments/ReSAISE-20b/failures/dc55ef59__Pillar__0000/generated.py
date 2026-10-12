import hashlib
import hmac

# A set of hash algorithms considered secure for HMAC usage.
# Excludes legacy or weak hashes such as md5, sha1, and other non‑cryptographic options.
_SECURE_HASH_ALGORITHMS = {
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
    "sha512_256",
}

# Secret key used for HMAC generation.
# In a real application this should be stored securely (e.g., in an environment variable
# or a dedicated secrets manager) and not hard‑coded.
SECRET_KEY = b"super_secret_key"


def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature for *message* using the hash algorithm named
    *algo_name*.  Only secure algorithms are permitted.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use (e.g., "sha256").
    message : bytes
        The raw input data to be signed.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If *algo_name* is not a supported or allowed hash algorithm.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = algo_name.lower()

    if algo not in _SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name}")

    # Verify that the chosen algorithm is available in hashlib
    try:
        hash_func = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm not available: {algo_name}") from exc

    # Compute the HMAC using the secret key and the chosen hash function
    return hmac.new(SECRET_KEY, message, digestmod=hash_func).digest()