import hashlib

# Secure algorithms that are acceptable for password hashing
_SECURE_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    # The following are considered secure enough for hashing,
    # but are not recommended as default password hash functions.
    "sha512_224",
    "sha512_256",
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use. Must be one of the secure algorithms
        listed in ``_SECURE_ALGORITHMS``.
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not in ``_SECURE_ALGORITHMS`` or is not
        available in the current Python runtime.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algorithm_name}' is not allowed or is considered insecure."
        )

    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Algorithm '{algorithm_name}' is not available in this Python runtime."
        )

    # Encode the password as UTF-8 before hashing
    pwd_bytes = pwd.encode("utf-8")

    # Create a new hash object and update it with the password
    hasher = hashlib.new(algo)
    hasher.update(pwd_bytes)

    return hasher.digest()