import hashlib

# Allowed hash algorithms (based on the provided list)
ALLOWED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512', 'sha3_224'
}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use.
    raw_password : str
        The plaintext password.

    Returns
    -------
    str
        The hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If an unsupported hash algorithm is specified.
    """
    if algorithm_name not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            f"Supported algorithms: {', '.join(sorted(ALLOWED_ALGORITHMS))}"
        )

    # Encode the password to bytes (UTF-8 is a safe default)
    password_bytes = raw_password.encode('utf-8')

    # Create the hash object
    try:
        hasher = hashlib.new(algorithm_name)
    except ValueError as exc:
        # In case the algorithm name is technically supported by hashlib
        # but not available in this environment
        raise ValueError(f"Hash algorithm '{algorithm_name}' is unavailable: {exc}") from exc

    # Update the hasher with the password bytes
    hasher.update(password_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()