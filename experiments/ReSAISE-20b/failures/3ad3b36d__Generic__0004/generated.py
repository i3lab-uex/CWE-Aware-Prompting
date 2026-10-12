import hashlib

# Set of supported hash algorithms provided by hashlib
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal representation.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use.
    raw_password : str
        The password string to be hashed.

    Returns
    -------
    str
        Hexadecimal hash of the password.

    Raises
    ------
    ValueError
        If `algorithm_name` is not in the list of supported algorithms.
    """
    # Normalize algorithm name to lowercase
    algo = algorithm_name.lower()

    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            f"Supported algorithms: {', '.join(sorted(SUPPORTED_ALGORITHMS))}"
        )

    # Encode the password to bytes (UTF-8 is a common choice)
    pwd_bytes = raw_password.encode('utf-8')

    # Create the hash object and compute hexdigest
    hasher = hashlib.new(algo)
    hasher.update(pwd_bytes)

    return hasher.hexdigest()