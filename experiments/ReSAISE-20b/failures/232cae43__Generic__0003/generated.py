import hashlib
import hmac

# Set of hash algorithms supported by the standard library's hashlib
SUPPORTED_ALGORITHMS = {
    'sha512', 'sha256', 'blake2s', 'ripemd160', 'sm3',
    'sha1', 'md5', 'sha512_256', 'shake_128', 'blake2b',
    'sha384', 'sha224', 'md5-sha1', 'shake_256',
    'sha512_224', 'sha3_256', 'sha3_512', 'sha3_224',
    'sha3_384'
}


def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature of the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        Data to be signed.
    secret : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported.
    """
    # Normalise algorithm name to lower case
    algo_name = hash_algorithm.lower()

    if algo_name not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Retrieve the constructor for the requested hash function
    try:
        hash_func = getattr(hashlib, algo_name)
    except AttributeError:
        # This should not happen because we checked the set above
        raise ValueError(f"Hash function {hash_algorithm} not available in hashlib")

    # Compute the HMAC digest
    return hmac.new(secret, payload, digestmod=hash_func).digest()