import hashlib

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    user_pass : bytes
        Password to hash.  It must be a byte string; callers should encode any
        Unicode password before passing it.

    Returns
    -------
    bytes
        The binary digest produced by the chosen hash algorithm.

    Raises
    ------
    ValueError
        If `algorithm_name` is not supported by the current Python installation.
    """
    # Normalise algorithm name to lower case as required by hashlib
    algo = algorithm_name.lower()

    # Use a whitelist of algorithms that are considered acceptable.
    # In practice, avoid weak hashes such as md5 or sha1 for password storage.
    accepted_algorithms = {
        'sha512_256', 'sha224', 'sha384', 'sha512_224',
        'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
        'sha256', 'blake2b', 'md5-sha1', 'shake_256',
        'ripemd160', 'md5', 'sha3_256', 'blake2s',
        'sha3_512', 'sha3_224'
    }

    if algo not in accepted_algorithms:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Compute the hash
    hasher = hashlib.new(algo, user_pass)
    return hasher.digest()