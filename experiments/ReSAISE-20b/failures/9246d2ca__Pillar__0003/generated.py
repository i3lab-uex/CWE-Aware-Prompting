import hashlib

# List of algorithms that hashlib supports on this platform.
SUPPORTED_ALGORITHMS = {
    "sha512_256", "sha224", "sha384", "sha512_224",
    "sha512", "sm3", "sha1", "sha3_384",
    "shake_128", "sha256", "blake2b", "md5-sha1",
    "shake_256", "ripemd160", "md5", "sha3_256",
    "blake2s", "sha3_512", "sha3_224"
}

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use. Must be one of ``SUPPORTED_ALGORITHMS``.
    pass_key : bytes
        The password (or key) to hash.

    Returns
    -------
    bytes
        The raw digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If ``algo_name`` is not in the list of supported algorithms.
    """
    algo = algo_name.lower()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algo_name!r}")

    # ``hashlib.new`` returns a new hash object for the requested algorithm.
    h = hashlib.new(algo)
    h.update(pass_key)
    return h.digest()