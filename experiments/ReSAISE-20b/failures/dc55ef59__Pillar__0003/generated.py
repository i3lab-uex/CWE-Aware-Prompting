import hashlib
import hmac

# ----------------------------------------------------------------------
# NOTE: The secret key must be generated and stored securely (e.g.
# using a hardware security module or a protected key store).
# ----------------------------------------------------------------------
secret_key: bytes = b"your-secure-secret-key"

# List of hash algorithms that are considered secure for HMAC usage.
SECURE_ALGORITHMS = {
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

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature of *message* using the hash algorithm
    specified by *algo_name*.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g. 'sha256').
    message : bytes
        Raw data that will be signed.

    Returns
    -------
    bytes
        The resulting HMAC digest.

    Raises
    ------
    ValueError
        If *algo_name* is not a supported or secure algorithm.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = algo_name.lower()

    # Verify that the requested algorithm is available in hashlib and
    # is on our list of secure algorithms.
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algo_name}")

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available in this Python build")

    # Compute the HMAC digest
    hmac_obj = hmac.new(secret_key, message, digestmod=algo)
    return hmac_obj.digest()