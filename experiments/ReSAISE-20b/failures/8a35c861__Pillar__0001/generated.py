import hashlib

# A set of algorithms considered cryptographically secure for hashing passwords.
# Weak algorithms such as md5, sha1, and sm3 are excluded.
_SECURE_ALGORITHMS = {
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
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Hash a password using a specified cryptographic algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use. Must be one of the secure algorithms.
    pw : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest as a byte sequence.

    Raises
    ------
    ValueError
        If the requested algorithm is not available or is considered insecure.
    """
    # Normalize the algorithm name to lower case as hashlib uses lower-case names
    algo_name = algo_name.lower()

    # Ensure the algorithm is in our whitelist of secure algorithms
    if algo_name not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algo_name}' is not in the list of secure algorithms."
        )

    # Verify that the algorithm is actually supported by this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Algorithm '{algo_name}' is not available in this hashlib installation."
        )

    # Create a new hash object and feed the password (encoded as UTF-8)
    hasher = hashlib.new(algo_name)
    hasher.update(pw.encode("utf-8"))
    return hasher.digest()