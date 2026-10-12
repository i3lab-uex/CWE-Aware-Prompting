import hashlib

# A set of algorithms considered cryptographically secure for hashing passwords.
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
    # SHAKE algorithms can be used with a custom digest size; here we allow them as well.
    "shake_128",
    "shake_256",
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        The name of the hash algorithm to use. Must be one of the secure algorithms defined in SECURE_ALGORITHMS.
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If `algo_hash` is not in SECURE_ALGORITHMS or if the algorithm is unavailable on the current platform.
    """
    algo_hash = algo_hash.lower()

    if algo_hash not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is not permitted or available. "
                         f"Allowed algorithms: {sorted(SECURE_ALGORITHMS)}")

    try:
        # For SHAKE functions, the user can specify a digest size; we default to 32 bytes.
        if algo_hash in {"shake_128", "shake_256"}:
            # SHAKE functions require a size argument; using 32 bytes (256 bits) as a default.
            hash_obj = hashlib.new(algo_hash, pwd_input.encode())
            return hash_obj.digest(32)
        else:
            hash_obj = hashlib.new(algo_hash, pwd_input.encode())
            return hash_obj.digest()
    except ValueError as exc:
        # This exception is raised if the algorithm name is not supported by hashlib.
        raise ValueError(f"Hash algorithm '{algo_hash}' is unavailable on this platform.") from exc