import hashlib

# List of algorithms that are considered secure for password hashing.
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512', 'sha3_224'
}

def hash_user_password(algorithm_name: str, user_pass: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha512', 'blake2b').
    user_pass : bytes
        The password to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported.
    """
    # Normalize algorithm name (hashlib accepts lower‑case names)
    alg = algorithm_name.lower()

    if alg not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(alg)
    hasher.update(user_pass)

    return hasher.digest()