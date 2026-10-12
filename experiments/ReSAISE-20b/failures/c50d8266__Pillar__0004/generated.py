import hashlib
import hmac

# Define the set of cryptographically secure hash algorithms.
# Algorithms that are considered weak (MD5, SHA‑1, RIPEMD160) are omitted.
_SECURE_ALGORITHMS = {
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
    "sm3",           # SHA‑3 based, considered secure
    "shake_128",
    "shake_256",
}

def create_checksum(algorithm_name: str, message_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate a cryptographic signature for the given data using HMAC.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be one of the secure algorithms.
    message_data : bytes
        The raw data that needs to be signed.
    secret_key : bytes
        Key used for HMAC.

    Returns
    -------
    bytes
        The generated signature (HMAC digest).

    Raises
    ------
    ValueError
        If the algorithm is not supported or insecure.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in _SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Verify that hashlib supports the requested algorithm
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hashlib does not support algorithm: {algorithm_name}")

    # Create an HMAC object with the chosen hash function
    h = hmac.new(secret_key, msg=message_data, digestmod=getattr(hashlib, algo))
    return h.digest()