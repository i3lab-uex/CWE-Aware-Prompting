import hashlib
import hmac

# List of cryptographically secure hash algorithms supported by the standard library.
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'blake2b',
    'sha3_256',
    'sha256',
    'sm3',          # available on some platforms
    'sha3_224',
    'shake_128',
    'sha512',
    'sha512_224',
    'shake_256',
    'sha3_512',
    'blake2s',
    'sha3_384',
}

# Secret key used for HMAC signing. In a real application this should be stored securely.
SECRET_KEY = b'super_secret_key'  # placeholder – replace with a secure key in production


def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for `message` using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the desired hash algorithm (e.g., 'sha256').
    message : bytes
        Data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the message.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalize algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Create a new HMAC object using the chosen hash constructor
    try:
        hash_func = getattr(hashlib, algo)
    except AttributeError:
        # The algorithm exists in SECURE_ALGORITHMS but not in hashlib (unlikely)
        raise ValueError(f"Hash algorithm {algorithm_name} is unavailable on this platform")

    h = hmac.new(SECRET_KEY, digestmod=hash_func)
    h.update(message)
    return h.digest()