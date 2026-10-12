import hashlib

# List of algorithms considered secure for password hashing.
# Excludes known weak/obsolete algorithms such as md5, sha1, ripemd160,
# and those not recommended for password storage (e.g., sha224).
SECURE_ALGORITHMS = {
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
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use.
    pwd : str
        Plain‑text password.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the algorithm is not supported or considered insecure.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algorithm_name}' is not available or considered insecure."
        )

    # Ensure the algorithm exists in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Algorithm '{algorithm_name}' is not available in the current hashlib implementation."
        )

    # Create a new hash object and feed it the password
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode("utf-8"))
    return hasher.digest()