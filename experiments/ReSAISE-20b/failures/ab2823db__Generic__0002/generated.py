import hashlib

# Set of supported hash algorithms from the problem description
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512',
    'sha3_224'
}

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hashes a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use.
    secret : str
        Plaintext password.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `algo_name` is not supported or unavailable in the current environment.
    """
    if algo_name.lower() not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{algo_name}'. "
            "Supported algorithms are: "
            + ", ".join(sorted(SUPPORTED_ALGORITHMS))
        )

    try:
        # Create a new hash object
        hasher = hashlib.new(algo_name)
    except (ValueError, TypeError) as exc:
        # Hashlib raises ValueError if algorithm is not available
        raise ValueError(
            f"Hash algorithm '{algo_name}' is unavailable in this environment."
        ) from exc

    # Encode the secret to bytes and update the hash object
    hasher.update(secret.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()