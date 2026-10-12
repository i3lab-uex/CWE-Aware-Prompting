import hashlib

# List of supported hash algorithms as per the description.
_SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hash a password using the specified hash algorithm and return its
    hexadecimal representation.

    Parameters
    ----------
    hash_type : str
        The name of the hash algorithm to use.
    pass_input : str
        The password string to be hashed.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If `hash_type` is not in the list of supported algorithms.
    """
    # Validate hash algorithm
    if hash_type.lower() not in _SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{hash_type}'. "
            f"Supported algorithms are: {', '.join(sorted(_SUPPORTED_ALGORITHMS))}"
        )

    # Create a new hash object and feed the password
    hash_obj = hashlib.new(hash_type.lower())
    hash_obj.update(pass_input.encode('utf-8'))

    # Return the hexadecimal digest
    return hash_obj.hexdigest()