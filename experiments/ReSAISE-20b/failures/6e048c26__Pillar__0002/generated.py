import hashlib

# List of algorithms supported by the current Python environment.
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512',
    'sha3_224'
}

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    user_pass : bytes
        The password data to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by this function.
    """
    # Normalise algorithm name to lowercase for case‑insensitive matching
    algo = algorithm_name.lower()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # Create a new hash object and feed the password bytes
    hasher = hashlib.new(algo)
    hasher.update(user_pass)

    # Return the raw digest (bytes)
    return hasher.digest()