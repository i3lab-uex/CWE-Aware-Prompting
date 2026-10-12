import hashlib

# All algorithms listed in the task description
SUPPORTED_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use.
    secret : str
        The plaintext password.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the algorithm is unsupported or unavailable.
    """
    # Normalise algorithm name to lower case
    algo_name = algo_name.lower()

    if algo_name not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algo_name}")

    # Some algorithms may not be available on the current platform
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_name}' is not available on this system")

    # Encode the secret to bytes; UTF-8 is a safe default
    data = secret.encode('utf-8')

    # Handle special case for SHAKE algorithms which require a digest size
    if algo_name.startswith('shake'):
        # Default to 64 bytes (512 bits) for SHAKE; can be changed if needed
        hash_obj = hashlib.new(algo_name, data)
        return hash_obj.hexdigest(64)

    # Standard fixed‑length algorithms
    hash_obj = hashlib.new(algo_name, data)
    return hash_obj.hexdigest()