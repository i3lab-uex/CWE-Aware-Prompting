import hashlib

# A curated set of secure hash algorithms (exclude md5, sha1, etc.)
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
    # cryptographic hash functions that are considered secure in current standards
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be in SECURE_ALGORITHMS.
    pwd : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest of the password.

    Raises
    ------
    ValueError
        If the algorithm is not available, or if it is not in the list of secure algorithms.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    # Ensure the chosen algorithm is explicitly allowed
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is not allowed or considered insecure.")

    # Verify that the algorithm is actually supported by the current Python build
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available on this system.")

    # Encode the password to bytes (UTF-8) before hashing
    pwd_bytes = pwd.encode("utf-8")

    # Compute the hash digest
    hasher = hashlib.new(algo)
    hasher.update(pwd_bytes)
    return hasher.digest()