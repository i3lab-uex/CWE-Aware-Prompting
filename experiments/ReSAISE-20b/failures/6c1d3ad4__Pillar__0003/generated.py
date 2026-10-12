import hashlib

# A curated set of algorithms considered secure for password hashing.
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "sha512_224",
    "sha512",
    "sm3",          # secure hash standard used in China
    "sha3_384",
    "shake_128",
    "sha256",
    "blake2b",
    "sha3_256",
    "blake2s",
    "sha3_512",
    "sha3_224",
    "shake_256",
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the requested algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the hash algorithm to use. Must be in SECURE_ALGORITHMS and available in hashlib.
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The binary digest of the hash.

    Raises
    ------
    ValueError
        If the algorithm is not in SECURE_ALGORITHMS or if it is not available on this system.
    """
    # Normalise the algorithm name (hashlib uses lowercase names)
    algo = algo_hash.lower()

    # Reject insecure or unsupported algorithms
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is not permitted or recognized as secure.")

    # Verify the algorithm exists in the current Python environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_hash}' is not available on this system.")

    # Create the hash object and feed it the password encoded as UTF‑8
    hash_obj = hashlib.new(algo)
    hash_obj.update(pwd_input.encode("utf-8"))

    # Return the raw digest bytes
    return hash_obj.digest()