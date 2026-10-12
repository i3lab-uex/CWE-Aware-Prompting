import hashlib

# Define a set of algorithms that are considered secure for this context.
SECURE_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha3_384', 'shake_128', 'sha256', 'blake2b',
    'md5-sha1', 'shake_256', 'ripemd160', 'sha3_256',
    'blake2s', 'sha3_512', 'sha3_224'
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (case‑insensitive).
    pwd : str
        The password string to be hashed.

    Returns
    -------
    bytes
        The raw hash digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or not in the secure list.
    """
    if not isinstance(algorithm_name, str) or not isinstance(pwd, str):
        raise TypeError("Both algorithm_name and pwd must be strings")

    algo = algorithm_name.lower()

    # Ensure the algorithm is in our secure list and available in hashlib
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is not considered secure")

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available on this system")

    # Compute the hash
    hasher = hashlib.new(algo, pwd.encode('utf-8'))
    return hasher.digest()