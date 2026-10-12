import hashlib
import hmac

# A secret key used for HMAC signing.
# In a real application this should be stored securely (e.g., in an environment variable or a secrets manager).
SECRET_KEY = b'\x01\x23\x45\x67\x89\xab\xcd\xef'  # example key, replace with a securely generated one

# Set of hash algorithms considered cryptographically secure for signing.
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'blake2b',
    'sha3_256',
    'sha256',
    'sm3',
    'sha3_224',
    'shake_128',
    'sha512',
    'sha512_224',
    'shake_256',
    'sha3_512',
    'blake2s',
    'sha3_384',
}

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or considered insecure.
    """
    # Normalize the algorithm name
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Verify that hashlib can provide the requested digest
    try:
        digestmod = getattr(hashlib, algo)
    except AttributeError as exc:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available in hashlib") from exc

    # Create the HMAC object and return the digest
    h = hmac.new(SECRET_KEY, message, digestmod=digestmod)
    return h.digest()