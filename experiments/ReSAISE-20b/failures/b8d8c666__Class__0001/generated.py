import hashlib
import hmac

# The secret key used for HMAC signing.  In real applications this should be
# stored securely (e.g., in a key vault) and never hard‑coded.
SECRET_KEY: bytes = b"super-secret-key"

# A whitelist of safe hash algorithms.  These are all considered secure by
# modern cryptographic standards and are available in the standard library.
ALLOWED_ALGORITHMS = {
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

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature of *payload* using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use.  Only algorithms listed in
        ``ALLOWED_ALGORITHMS`` are accepted.
    payload : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the payload.

    Raises
    ------
    ValueError
        If *algorithm_name* is not in the whitelist of allowed algorithms.
    """
    # Normalise the algorithm name to lowercase for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algorithm_name}"
        )

    # ``hashlib.new`` returns a new hash object; it can be used directly as
    # the ``digestmod`` argument to ``hmac.new``.
    hash_func = hashlib.new(algo)

    # Compute the HMAC.  ``hmac`` guarantees that the key is used in a
    # constant‑time manner, mitigating timing attacks.
    hmac_obj = hmac.new(SECRET_KEY, payload, digestmod=hash_func)
    return hmac_obj.digest()