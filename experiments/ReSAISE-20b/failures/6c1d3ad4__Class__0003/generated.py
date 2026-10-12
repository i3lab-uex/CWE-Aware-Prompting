import hashlib

# A set of cryptographic algorithms that are considered secure for hashing passwords.
# Weak algorithms such as md5, sha1, and sm3 are intentionally omitted.
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
    # Additional algorithms that are supported by hashlib and considered secure
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the cryptographic hash algorithm to use.
    pwd_input : str
        Password string to be hashed.

    Returns
    -------
    bytes
        The resulting hash value as a byte string.

    Raises
    ------
    ValueError
        If the chosen algorithm is not supported or is considered insecure.
    """
    if not isinstance(algo_hash, str) or not isinstance(pwd_input, str):
        raise TypeError("Both algo_hash and pwd_input must be strings")

    algo = algo_hash.lower()
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algo_hash}' is either not available or considered insecure."
        )

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_hash}' is not supported by the hashlib module.")

    # Create a new hash object and update it with the password bytes
    h = hashlib.new(algo)
    h.update(pwd_input.encode("utf-8"))
    return h.digest()