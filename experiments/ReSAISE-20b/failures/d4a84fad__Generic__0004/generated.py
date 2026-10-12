import hashlib

def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hash a password using the specified hash algorithm and return its hexadecimal representation.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use (e.g. 'sha256', 'md5').
    user_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If `encryption_method` is not a supported hash algorithm.
    """
    # List of supported algorithms as reported by hashlib.algorithms_available
    supported_algorithms = {
        'sha512_256', 'sha224', 'sha384', 'sha512_224',
        'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
        'sha256', 'blake2b', 'md5-sha1', 'shake_256',
        'ripemd160', 'md5', 'sha3_256', 'blake2s',
        'sha3_512', 'sha3_224'
    }

    # Normalize the algorithm name to lower case
    algo_name = encryption_method.lower()

    if algo_name not in supported_algorithms:
        raise ValueError(f"Unsupported hash algorithm: '{encryption_method}'. "
                         f"Supported algorithms are: {', '.join(sorted(supported_algorithms))}")

    # Create a new hash object
    hasher = hashlib.new(algo_name)
    # Encode the password to bytes (UTF-8 is standard for text hashing)
    hasher.update(user_password.encode('utf-8'))
    # Return the hexadecimal digest
    return hasher.hexdigest()