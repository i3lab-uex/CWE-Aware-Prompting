import hashlib

# A set of algorithms considered secure for password hashing purposes.
SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_224",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    # SM3 is considered secure in some contexts but not universally accepted; include if available
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be one of the secure algorithms listed in SECURE_ALGORITHMS.
    pwd : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the chosen algorithm is not available in hashlib or is considered insecure.
    """
    # Normalise algorithm name
    alg = algorithm_name.lower()

    if alg not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is not a supported secure hash algorithm.")

    try:
        hasher = hashlib.new(alg)
    except ValueError as exc:
        # The algorithm is not available in this Python build
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not supported by hashlib.") from exc

    # Encode password as UTF-8 before hashing
    hasher.update(pwd.encode("utf-8"))
    return hasher.digest()