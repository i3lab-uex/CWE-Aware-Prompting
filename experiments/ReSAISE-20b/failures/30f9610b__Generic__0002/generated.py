import hashlib
import hmac

# Define the set of supported hash algorithms.
SUPPORTED_ALGORITHMS = {
    'md5',
    'sha1',
    'sha256',
    'blake2b',
    'ripemd160',
    'sha512',
    'shake_256',
    'sm3',
    'sha384',
    'sha3_256',
    'sha512_224',
}

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Sign the provided message using HMAC with the specified hash algorithm and secret key.

    Parameters
    ----------
    method_name : str
        Name of the hash algorithm to use (e.g., 'sha256').
    data : bytes
        The message to be signed.
    secret_key : bytes
        Secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Normalise method name to lower case for comparison
    algo = method_name.lower()

    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {method_name}")

    # Ensure the algorithm is actually available in this Python build
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {method_name} is not available in this environment")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(secret_key, data, digestmod=algo)
    return hmac_obj.digest()