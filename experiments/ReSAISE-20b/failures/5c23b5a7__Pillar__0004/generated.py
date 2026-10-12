import hashlib

# A set of cryptographic algorithms considered acceptable for hashing passwords.
# Note: algorithms like md5 and sha1 are included in hashlib but are discouraged
# for password hashing due to known weaknesses. Users should prefer stronger
# algorithms such as sha256, sha512, or the SHA-3 family.
SUPPORTED_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "sha512_224",
    "sha512",
    "sm3",          # available on OpenSSL 1.1.1+ and some Python builds
    "sha256",
    "blake2b",
    "md5-sha1",     # rarely used; included for completeness
    "shake_128",
    "sha3_384",
    "sha1",         # discouraged
    "shake_256",
    "ripemd160",
    "md5",          # discouraged
    "sha3_256",
    "blake2s",
    "sha3_512",
    "sha3_224",
}

def secure_hash_password(algorithm_name: str, user_password: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    user_password : bytes
        The password to hash. Must be in byte form; callers should encode
        strings using a secure encoding such as UTF-8 before passing.

    Returns
    -------
    bytes
        The raw hash digest of the password.

    Raises
    ------
    ValueError
        If `algorithm_name` is not supported or if the algorithm cannot be found
        in the underlying OpenSSL/cryptography backend.
    """
    # Normalize algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            "Supported algorithms are: "
            + ", ".join(sorted(SUPPORTED_ALGORITHMS))
        )

    try:
        # hashlib.new accepts any algorithm name supported by the underlying
        # OpenSSL library. It will raise a ValueError if the algorithm is not found.
        hash_obj = hashlib.new(algo)
    except ValueError as exc:
        raise ValueError(
            f"Hash algorithm '{algorithm_name}' is not available in this environment."
        ) from exc

    hash_obj.update(user_password)
    return hash_obj.digest()