import hashlib

# Set of supported hash algorithms (as provided by the task description)
_SUPPORTED_HASHES = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512',
    'sha3_224'
}

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hash a password using the specified hash algorithm and return its hexadecimal representation.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use.
    user_password : str
        The password string to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the provided encryption_method is not supported.
    """
    if encryption_method.lower() not in _SUPPORTED_HASHES:
        raise ValueError(
            f"Unsupported hash function '{encryption_method}'. "
            "Supported algorithms are: " + ", ".join(sorted(_SUPPORTED_HASHES))
        )

    # Create a new hash object for the chosen algorithm
    hasher = hashlib.new(encryption_method.lower())

    # Update the hash object with the password encoded in UTF-8
    hasher.update(user_password.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()