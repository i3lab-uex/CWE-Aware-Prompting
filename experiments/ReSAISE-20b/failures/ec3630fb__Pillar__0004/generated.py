import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Hashes the given password using the specified hash algorithm and returns
    the hexadecimal digest.

    Args:
        hash_type: Name of the hash function to use (e.g. 'sha256', 'blake2b').
        secret:    The password string to hash.

    Returns:
        A hexadecimal string representing the hashed password.

    Raises:
        ValueError: If the specified hash algorithm is not supported by
                    hashlib or if it is considered insecure.
    """
    # Define a set of acceptable algorithms (exclude known weak ones)
    _SECURE_ALGORITHMS = {
        'sha224', 'sha256', 'sha384', 'sha512',
        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
        'blake2b', 'blake2s',
        'sha512_224', 'sha512_256'
    }

    # Normalise the algorithm name
    algo = hash_type.lower()

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_type}' is not available.")

    if algo not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Hash algorithm '{hash_type}' is considered insecure "
            "for password hashing. Use a stronger alternative."
        )

    # Perform the hash
    hasher = hashlib.new(algo)
    hasher.update(secret.encode('utf-8'))
    return hasher.hexdigest()