import hashlib

# Supported algorithms as listed in the description
_SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its
    hexadecimal representation.

    Parameters:
        algorithm_name (str): Name of the hash algorithm to use.
        raw_password   (str): The plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If the chosen algorithm is not supported.
    """
    # Normalise algorithm name to match the keys in _SUPPORTED_ALGORITHMS
    alg = algorithm_name.lower()
    if alg not in _SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported hash algorithm '{algorithm_name}'. "
            "Supported algorithms are: "
            + ", ".join(sorted(_SUPPORTED_ALGORITHMS))
        )

    # Encode the password to bytes (UTF-8 is a common choice)
    password_bytes = raw_password.encode('utf-8')

    # Create the hash object
    hasher = hashlib.new(alg, password_bytes)

    # Return hexadecimal digest
    return hasher.hexdigest()