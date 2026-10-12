import hashlib

# Set of supported hash algorithms as per the problem description
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its hexadecimal representation.

    Args:
        hash_type (str): The name of the hash algorithm to use.
        pass_input (str): The password string to be hashed.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If an unsupported hash algorithm is specified.
    """
    if hash_type not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {hash_type}")

    # Convert the password to bytes
    pwd_bytes = pass_input.encode('utf-8')

    # Create a new hash object with the specified algorithm
    try:
        hasher = hashlib.new(hash_type)
    except ValueError as exc:
        # This should not happen because we pre-validated the algorithm name
        raise ValueError(f"Hash creation failed for {hash_type}") from exc

    # Update the hash object with the password bytes
    hasher.update(pwd_bytes)

    # Return the hexadecimal digest
    return hasher.hexdigest()