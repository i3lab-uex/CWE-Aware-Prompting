import hashlib

# Set of hash algorithms supported by hashlib in this environment.
_SUPPORTED_HASHES = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns its
    hexadecimal representation.

    Parameters:
        hash_type (str): The name of the hash algorithm to use.
        pass_input (str): The password string to be hashed.

    Returns:
        str: Hexadecimal hash of the input password.

    Raises:
        ValueError: If `hash_type` is not a supported hash algorithm.
    """
    if hash_type not in _SUPPORTED_HASHES:
        raise ValueError(f"Unsupported hash algorithm: {hash_type!r}. "
                         f"Supported algorithms are: {sorted(_SUPPORTED_HASHES)}")

    # Create a new hash object for the specified algorithm
    hasher = hashlib.new(hash_type)

    # Encode the password to bytes (UTF-8) and update the hasher
    hasher.update(pass_input.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()