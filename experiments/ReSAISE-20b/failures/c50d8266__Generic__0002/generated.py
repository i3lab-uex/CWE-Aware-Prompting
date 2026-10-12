import hashlib
import hmac

# List of algorithms considered secure for HMAC usage.
_SECURE_ALGORITHMS = {
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'blake2b', 'blake2s', 'sha512_256'
}

def create_checksum(algorithm_name: str, message_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for `message_data` using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing algorithm to use. Must be one of the secure algorithms
        listed in `_SECURE_ALGORITHMS`.
    message_data : bytes
        The raw data that needs to be signed.
    secret_key : bytes
        Secret key used for the HMAC computation.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not in `_SECURE_ALGORITHMS` or is unsupported by
        `hashlib`.
    """
    # Normalise the algorithm name to lowercase for comparison.
    algo = algorithm_name.lower()

    if algo not in _SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure algorithm: {algorithm_name}")

    # Ensure the algorithm is available in hashlib.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available in the current hashlib build.")

    # Create a new HMAC object with the chosen hash function.
    hmac_obj = hmac.new(secret_key, message_data, digestmod=algo)

    return hmac_obj.digest()