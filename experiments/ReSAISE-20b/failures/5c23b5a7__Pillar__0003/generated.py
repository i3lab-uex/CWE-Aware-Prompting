import hashlib

# List of supported algorithms (kept in sync with hashlib.algorithms_available)
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512',
    'sha3_224'
}

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use. Must be one of the supported algorithms.
    user_password : bytes
        Password to hash.

    Returns
    -------
    bytes
        The raw digest value produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the supported list.
    """
    # Normalise algorithm name to lower case to match hashlib's names
    algo = algorithm_name.lower()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:
        # Defensive: in case the algorithm name is syntactically wrong
        raise ValueError(f"Invalid hash algorithm: {algorithm_name}") from exc

    # Feed the password into the hash function
    hasher.update(user_password)

    # Return the digest bytes
    return hasher.digest()