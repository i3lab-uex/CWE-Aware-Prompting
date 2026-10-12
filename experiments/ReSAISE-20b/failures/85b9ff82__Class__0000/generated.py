import hashlib
import hmac

# Define the secret key used for HMAC. In real usage this should be a
# securely generated random value and kept confidential.
SECRET_KEY = b"super_secret_key"

# A set of cryptographically strong hash algorithms.  Weak or legacy
# algorithms (e.g., MD5, SHA‑1, RIPEMD‑160) are intentionally omitted
# to avoid CWE‑327.
ALLOWED_HASHES = {
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
    Create an HMAC signature of *content* using the specified
    hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256').
    content : bytes
        Raw data that will be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If *hash_algorithm* is not in the set of allowed algorithms.
    """
    # Normalise the algorithm name to lower case for comparison
    algo_name = hash_algorithm.lower()

    if algo_name not in ALLOWED_HASHES:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {hash_algorithm}"
        )

    # Verify that the requested algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Hash algorithm {hash_algorithm} is not available in this Python build"
        )

    # Compute the HMAC using the chosen algorithm
    signature = hmac.new(
        key=SECRET_KEY,
        msg=content,
        digestmod=algo_name
    ).digest()

    return signature