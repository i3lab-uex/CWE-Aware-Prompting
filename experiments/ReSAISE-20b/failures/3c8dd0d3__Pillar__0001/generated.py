import hashlib

# Whitelist of secure algorithms (exclude weak ones like md5, sha1)
_SECURE_ALGORITHMS = {
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
    'sha512_224',
    'sha512_256',
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hashes a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use. Must be one of the secure algorithms.
    pwd : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest of the password.

    Raises
    ------
    ValueError
        If the chosen algorithm is not in the secure whitelist or is not supported by hashlib.
    """
    # Normalise the algorithm name to lower case
    algo = algorithm_name.lower()

    if algo not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algorithm_name}' is not allowed. "
            "Choose one of the following secure algorithms: "
            f"{', '.join(sorted(_SECURE_ALGORITHMS))}"
        )

    try:
        # Create a new hash object
        hasher = hashlib.new(algo)
    except ValueError as exc:
        # Raised if the algorithm is not supported by the underlying OpenSSL
        raise ValueError(
            f"Algorithm '{algorithm_name}' is not available in this Python environment."
        ) from exc

    # Encode the password as UTF‑8 and update the hash
    hasher.update(pwd.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()