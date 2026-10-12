import hashlib
import hmac

# A secret key that must be kept confidential.
# In a real application this would come from secure storage or an environment variable.
SECRET_KEY = b"super-secret-key"

# Only these hash algorithms are considered secure for HMAC usage.
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
    Create an HMAC signature of `payload` using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be one of ALLOWED_ALGORITHMS.
    payload : bytes
        The data to sign.

    Returns
    -------
    bytes
        The HMAC digest of the payload.

    Raises
    ------
    ValueError
        If `algorithm_name` is not in ALLOWED_ALGORITHMS.
    """
    if algorithm_name.lower() not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algorithm_name}")

    # hmac accepts the digest name directly
    return hmac.new(SECRET_KEY, payload, algorithm_name.lower()).digest()