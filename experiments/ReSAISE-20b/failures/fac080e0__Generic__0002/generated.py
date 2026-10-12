import hashlib
import hmac

# Set of algorithms we explicitly support (can be extended as needed)
SUPPORTED_ALGORITHMS = {
    'sha512', 'sha256', 'blake2s', 'ripemd160',
    'sm3', 'md5', 'sha3_256', 'sha512_224',
    'sha1', 'sha384'
}

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of `msg` using `secret_key` and the specified hash algorithm.

    Parameters
    ----------
    algo : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        Secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the chosen algorithm is not supported on this system.
    """
    # Normalize algorithm name (hashlib uses lower case names)
    algo_lower = algo.lower()

    # Check that the algorithm is available in hashlib
    if algo_lower not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Verify that hashlib can actually provide the requested digest
    if algo_lower not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo}' is not available on this system")

    # Compute the HMAC digest
    hmac_obj = hmac.new(secret_key, msg, digestmod=algo_lower)
    return hmac_obj.digest()