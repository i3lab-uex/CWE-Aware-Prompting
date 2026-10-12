import hashlib

# List of algorithms considered cryptographically strong for password hashing.
# Excludes legacy weak hashes such as md5 and sha1.
_STRENGTH_REQUIREMENT = {
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

# Algorithms that are available on the current system (case‑insensitive).
_AVAILABLE_ALGS = {alg.lower() for alg in hashlib.algorithms_available}


def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of a hash algorithm supported by the current Python installation.
    pwd : str
        The plaintext password to be hashed.

    Returns
    -------
    bytes
        The raw digest produced by the chosen hash algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on the system or if it is
        considered insecure for password hashing.
    """
    if not isinstance(algo_name, str) or not isinstance(pwd, str):
        raise TypeError("Both algo_name and pwd must be strings")

    algo = algo_name.lower()

    # Verify algorithm availability
    if algo not in _AVAILABLE_ALGS:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported on this system")

    # Enforce a minimal security level
    if algo not in _STRENGTH_REQUIREMENT:
        raise ValueError(f"Hash algorithm '{algo_name}' is considered weak for password hashing")

    # Create the hash object and digest
    try:
        hasher = hashlib.new(algo)
    except Exception as exc:   # pragma: no cover
        raise ValueError(f"Failed to initialize hash algorithm '{algo_name}': {exc}") from exc

    hasher.update(pwd.encode("utf-8"))
    return hasher.digest()