import hashlib

# Set of supported hash algorithm names (as provided by the description)
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    secret : str
        The plaintext password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `algo_name` is not supported or unavailable in the current environment.
    """
    # Normalise algorithm name to lower case for consistency
    algo_name = algo_name.lower()

    if algo_name not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algo_name}")

    try:
        # Create a new hash object for the requested algorithm
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        # In case the algorithm name is valid but not available in this Python build
        raise ValueError(f"Hash algorithm '{algo_name}' is unavailable: {exc}") from exc

    # Encode the secret to bytes; UTF-8 is a safe default
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()