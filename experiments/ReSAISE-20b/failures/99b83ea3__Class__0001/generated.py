import hashlib
import hmac

# A secret key used for HMAC signing. In a real application this should be
# stored securely (e.g., environment variable, key management service).
SECRET_KEY = b"super_secret_key"

# Only include cryptographically secure hash algorithms.
ALLOWED_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",
    "sha3_224",
    "shake_128",
    "sha512",
    "sha512_224",
    "shake_256",
    "sha3_512",
    "blake2s",
    "sha3_384",
}

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for *message* using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (must be in ALLOWED_ALGORITHMS).
    message : bytes
        The data to sign.

    Returns
    -------
    bytes
        The HMAC signature.

    Raises
    ------
    ValueError
        If *algorithm_name* is not in the list of allowed, secure algorithms.
    """
    if algorithm_name.lower() not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Ensure the chosen algorithm is available in hashlib
    try:
        hash_func = hashlib.new(algorithm_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm not supported by hashlib: {algorithm_name}") from exc

    # Use HMAC with the chosen hash function
    signature = hmac.new(SECRET_KEY, message, digestmod=hash_func).digest()
    return signature