import hashlib

# List of supported hash algorithms as provided by the task description.
SUPPORTED_HASHES = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hashes a password using the specified algorithm and returns the
    hexadecimal digest.

    Parameters
    ----------
    hash_type : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pass_input : str
        The plaintext password to hash.

    Returns
    -------
    str
        The hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If ``hash_type`` is not one of the supported algorithms.
    """
    # Normalise the algorithm name to match hashlib's expected format
    algo = hash_type.lower()

    if algo not in SUPPORTED_HASHES:
        raise ValueError(
            f"Unsupported hash algorithm '{hash_type}'. "
            f"Supported algorithms: {', '.join(sorted(SUPPORTED_HASHES))}"
        )

    # Some algorithms like 'shake_128' and 'shake_256' require a digest size.
    # For these we default to 64 bytes (512 bits) for consistency.
    if algo in ('shake_128', 'shake_256'):
        digest_size = 64
        hash_obj = hashlib.new(algo, pass_input.encode('utf-8'), digest_size=digest_size)
        return hash_obj.hexdigest()
    else:
        # For all other algorithms, the default digest size is used.
        hash_obj = hashlib.new(algo)
        hash_obj.update(pass_input.encode('utf-8'))
        return hash_obj.hexdigest()