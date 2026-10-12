import hashlib

# Set of algorithms explicitly supported by the task description
_SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the requested algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use.
    user_pass : bytes
        The password (in binary form) to be hashed.

    Returns
    -------
    bytes
        Digest of the password computed with the chosen algorithm.

    Raises
    ------
    ValueError
        If `algorithm_name` is not in the list of supported algorithms.
    """
    if algorithm_name not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # hashlib.new accepts the algorithm name and returns a new hash object
    try:
        hasher = hashlib.new(algorithm_name)
    except (TypeError, ValueError) as exc:
        # This should not happen because we validated the name,
        # but guard against future changes in hashlib.
        raise ValueError(f"Failed to create hash object for algorithm {algorithm_name!r}") from exc

    hasher.update(user_pass)
    return hasher.digest()