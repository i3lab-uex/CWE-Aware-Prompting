import hashlib
import hmac

# Allowed hash algorithms as specified in the description
ALLOWED_ALGORITHMS = {
    'sha512', 'sha256', 'blake2s', 'ripemd160',
    'sm3', 'md5', 'sha3_256', 'sha512_224',
    'sha1', 'sha384'
}

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use.
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key used for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or is considered insecure.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    # Check if the algorithm is in our allowed list and supported by hashlib
    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm '{algorithm_name}'. "
                         f"Allowed algorithms: {sorted(ALLOWED_ALGORITHMS)}")

    # Verify that hashlib actually supports the algorithm on this platform
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available on this system.")

    # Create HMAC object using the specified algorithm
    h = hmac.new(secret_key, msg=msg_content, digestmod=algo)

    # Return the raw bytes of the HMAC digest
    return h.digest()