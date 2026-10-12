import hashlib

# A whitelist of cryptographic hash algorithms that are considered secure for password hashing.
SECURE_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
    # SHA-512/256 and SHA-512/224 are also considered secure
    'sha512_256',
    'sha512_224',
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use. Must be one of the secure algorithms
        listed in :data:`SECURE_ALGORITHMS`. Case-sensitive.
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available or is not in the whitelist.
    """
    # Normalise input to avoid accidental mismatches
    alg = algorithm_name.strip()

    if alg not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure algorithm '{alg}'. "
            f"Allowed algorithms: {', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Ensure the algorithm is available in hashlib
    try:
        hasher = hashlib.new(alg)
    except ValueError as exc:
        raise ValueError(f"Algorithm '{alg}' is not available in this Python build.") from exc

    # Encode the password to bytes and update the hash
    hasher.update(pwd.encode('utf-8'))

    return hasher.digest()