import hashlib

# List of algorithms supported by the specification (may vary per Python version)
ALLOWED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Return the hexadecimal hash of a password using the specified algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If ``hash_algo`` is not supported or unavailable in the current Python
        environment.
    """
    # Normalise algorithm name (hashlib is case‑insensitive but we keep it lower)
    algo = hash_algo.lower()

    # Verify algorithm is explicitly allowed
    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{hash_algo}'. "
            "Allowed algorithms: " + ", ".join(sorted(ALLOWED_ALGORITHMS))
        )

    # Verify that the algorithm is available in this runtime
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"The algorithm '{hash_algo}' is not available in this Python "
            "runtime. Please ensure it is supported by the underlying OpenSSL."
        )

    # Perform hashing
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))
    return hasher.hexdigest()