import hashlib

# Define a set of algorithms considered sufficiently secure for password hashing.
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'sha512_224',
    'sha512',
    'sm3',
    'sha3_384',
    'shake_128',   # requires a length argument when hashing
    'sha256',
    'blake2b',
    'shake_256',   # requires a length argument when hashing
    'ripemd160',
    'sha3_256',
    'blake2s',
    'sha3_512',
    'sha3_224',
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use.
    pwd : str
        The password string to be hashed.

    Returns
    -------
    bytes
        The raw digest of the hash function applied to `pwd`.

    Raises
    ------
    ValueError
        If the chosen algorithm is not in the secure list or not available in hashlib.
    """
    if algorithm_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is not considered secure or is unsupported.")

    # Some algorithms (shake_128/256) require a digest length argument.
    if algorithm_name in {'shake_128', 'shake_256'}:
        # For password hashing, 32 bytes (256 bits) is a common choice.
        digest_len = 32
        hasher = hashlib.new(algorithm_name)
        hasher.update(pwd.encode('utf-8'))
        return hasher.digest(digest_len)

    try:
        hasher = hashlib.new(algorithm_name)
    except ValueError as exc:
        # This should not happen if SECURE_ALGORITHMS is correct,
        # but we handle it defensively.
        raise ValueError(f"Algorithm '{algorithm_name}' is not available in hashlib.") from exc

    hasher.update(pwd.encode('utf-8'))
    return hasher.digest()