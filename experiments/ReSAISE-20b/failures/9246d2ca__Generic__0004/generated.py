import hashlib

# List of supported hash algorithms as documented by hashlib.algorithms_available
_SUPPORTED_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "sha512_224",
    "sha512",
    "sm3",
    "sha1",
    "sha3_384",
    "shake_128",
    "sha256",
    "blake2b",
    "md5-sha1",
    "shake_256",
    "ripemd160",
    "md5",
    "sha3_256",
    "blake2s",
    "sha3_512",
    "sha3_224",
}

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use. Must be one of the algorithms listed in
        :data:`_SUPPORTED_ALGORITHMS`. The comparison is case-sensitive.
    pass_key : bytes
        The password (or key) to hash.

    Returns
    -------
    bytes
        The binary digest produced by the chosen hash algorithm.

    Raises
    ------
    ValueError
        If *algo_name* is not in :data:`_SUPPORTED_ALGORITHMS`.
    """
    if algo_name not in _SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm '{algo_name}'. "
            f"Supported algorithms are: {sorted(_SUPPORTED_ALGORITHMS)}"
        )

    # Use hashlib.new to create a hash object with the requested algorithm.
    hasher = hashlib.new(algo_name)
    hasher.update(pass_key)
    return hasher.digest()