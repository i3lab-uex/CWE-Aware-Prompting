import hashlib
import hmac

# A secret key used for signing. In a real application this should be stored
# securely (e.g., in an HSM or environment variable) and never hard‑coded.
SECRET_KEY = b'super_secret_key_that_is_at_least_32_bytes_long'

# Secure hash algorithms that are acceptable for HMAC.
ALLOWED_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'sha512',
    'sm3',
    'sha3_384',
    'shake_128',   # note: SHAKE can be used as a variable‑length hash
    'sha256',
    'blake2b',
    'shake_256',
    'ripemd160',
    'sha3_256',
    'blake2s',
    'sha3_512',
    'sha3_224',
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for `message` using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hashing algorithm to use. Must be one of the secure algorithms
        listed in `ALLOWED_ALGORITHMS`.
    message : bytes
        The raw data that needs to be signed.

    Returns
    -------
    bytes
        The HMAC digest for the provided data.

    Raises
    ------
    ValueError
        If `algorithm` is not supported or considered insecure.
    """
    if algorithm.lower() not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure algorithm '{algorithm}'. "
            "Allowed algorithms: " + ", ".join(sorted(ALLOWED_ALGORITHMS))
        )

    # Verify that the algorithm is actually available in hashlib
    if not hasattr(hashlib, algorithm):
        raise ValueError(f"Hash algorithm '{algorithm}' is not available in hashlib.")

    # Create HMAC object using the chosen digest mode
    hmac_obj = hmac.new(SECRET_KEY, message, digestmod=algorithm)
    return hmac_obj.digest()