import hashlib

# Supported hash algorithms (case‑insensitive)
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}


def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its hexadecimal representation.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use.
    user_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If an unsupported or unknown hash algorithm is supplied.
    """
    if not isinstance(encryption_method, str) or not isinstance(user_password, str):
        raise TypeError("Both encryption_method and user_password must be strings")

    algo = encryption_method.lower()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{encryption_method}'. "
            "Supported algorithms are: " + ", ".join(sorted(SUPPORTED_ALGORITHMS))
        )

    # Create a new hash object
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        # This should not happen because we validated the algorithm, but be defensive.
        raise ValueError(f"Hash algorithm '{encryption_method}' is not available on this system") from exc

    # Update the hasher with the password bytes
    hasher.update(user_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()