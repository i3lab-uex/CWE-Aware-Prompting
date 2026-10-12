import hashlib

# List of hash algorithms that hashlib supports in this environment
_SUPPORTED_HASHES = {
    'sha512_256',
    'sha224',
    'sha384',
    'sha512_224',
    'sha512',
    'sm3',
    'sha1',
    'sha3_384',
    'shake_128',
    'sha256',
    'blake2b',
    'md5-sha1',
    'shake_256',
    'ripemd160',
    'md5',
    'sha3_256',
    'blake2s',
    'sha3_512',
    'sha3_224'
}

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its
    hexadecimal representation.

    Parameters:
        hash_type (str): Name of the hash algorithm to use.
        pass_input (str): The plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If the specified hash algorithm is not supported.
    """
    if hash_type not in _SUPPORTED_HASHES:
        raise ValueError(
            f"Unsupported hash algorithm '{hash_type}'. "
            f"Supported algorithms: {', '.join(sorted(_SUPPORTED_HASHES))}"
        )

    # Create a new hash object. Using `hashlib.new` ensures that the
    # algorithm is looked up by name, preventing accidental misuse of
    # hardcoded hash functions.
    hasher = hashlib.new(hash_type)

    # Encode the password as UTF-8 bytes before hashing.
    hasher.update(pass_input.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()