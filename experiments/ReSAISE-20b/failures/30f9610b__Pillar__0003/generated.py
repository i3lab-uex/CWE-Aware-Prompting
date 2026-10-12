import hashlib
import hmac

# List of supported hash algorithm names for quick reference
SUPPORTED_ALGORITHMS = {
    'md5', 'sha1', 'sha256', 'blake2b',
    'ripemd160', 'sha512', 'shake_256', 'sm3',
    'sha384', 'sha3_256', 'sha512_224'
}

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Sign the provided message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hashing function to use (e.g., 'sha256', 'md5').
    data : bytes
        The message to be signed.
    secret_key : bytes
        Secret key used in the HMAC process.

    Returns
    -------
    bytes
        The generated HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Normalise the method name (case-insensitive)
    algo = method_name.lower()

    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {method_name}")

    # Ensure the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{method_name}' is not available on this system")

    # Create the HMAC object using the chosen digest
    hmac_obj = hmac.new(secret_key, data, digestmod=hashlib.new(algo))
    return hmac_obj.digest()