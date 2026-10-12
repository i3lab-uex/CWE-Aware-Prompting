import hashlib

# List of secure algorithms (exclude md5, sha1, ripemd160, etc.)
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
    # Additional optional secure algorithms (if available)
    "sm3",          # used in Chinese standards
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the given password using a secure algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256').
    pw : str
        Password string to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If the algorithm is not available or considered insecure.
    """
    # Normalise algorithm name
    algo_name = algo_name.lower()

    # Check if the algorithm is in our whitelist of secure algorithms
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is either unavailable or not considered secure.")

    # Ensure the algorithm is supported by hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_name}' is not supported by the current hashlib implementation.")

    # Compute hash
    hasher = hashlib.new(algo_name)
    hasher.update(pw.encode("utf-8"))
    return hasher.digest()