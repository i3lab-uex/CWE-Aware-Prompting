import hashlib

# Define the set of algorithms that are considered secure for password hashing.
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
    # The SM3 algorithm is considered secure in some contexts but may not be available
    # everywhere. It is included only if present in hashlib.
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using a secure algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm to use.
    pw : str
        Password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib or is not in the list
        of secure algorithms.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algo_name.lower()

    # Check that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_name}' is not available in hashlib.")

    # Check that the algorithm is considered secure
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is considered insecure for password hashing.")

    # Compute the hash
    hasher = hashlib.new(algo)
    hasher.update(pw.encode("utf-8"))
    return hasher.digest()