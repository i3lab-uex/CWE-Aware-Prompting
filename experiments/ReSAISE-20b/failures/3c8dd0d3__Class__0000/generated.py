import hashlib

# A set of algorithms considered secure for password hashing.
SECURE_ALGORITHMS = {
    "sha224", "sha256", "sha384", "sha512",
    "sha3_224", "sha3_256", "sha3_384", "sha3_512",
    "blake2b", "blake2s",
    # Extendable-output functions (XOF) are also acceptable
    "shake_128", "shake_256",
}

# Include any algorithm that is available in the current hashlib implementation
# but not explicitly marked as insecure.
AVAILABLE_ALGORITHMS = set(hashlib.algorithms_available)

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the algorithm is not available or considered insecure.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in AVAILABLE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available.")

    # Reject known weak algorithms
    if algo in {"md5", "sha1", "ripemd160"}:
        raise ValueError(f"Algorithm '{algorithm_name}' is insecure and not allowed.")

    # Allow only algorithms explicitly marked as secure
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is not considered secure for password hashing.")

    # Compute the hash
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode("utf-8"))
    return hasher.digest()