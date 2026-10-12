import hashlib

# List of supported hash algorithms as per the specification
_SUPPORTED_HASHES = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224',
    'sha512', 'sm3', 'sha1', 'sha3_384', 'shake_128',
    'sha256', 'blake2b', 'md5-sha1', 'shake_256',
    'ripemd160', 'md5', 'sha3_256', 'blake2s',
    'sha3_512', 'sha3_224'
}

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hashes a password using the specified hash algorithm and returns
    the hexadecimal digest.

    Parameters:
        hash_type (str): Name of the hash algorithm to use.
        pass_input (str): The plaintext password.

    Returns:
        str: Hexadecimal representation of the hashed password.

    Raises:
        ValueError: If an unsupported hash algorithm is requested.
    """
    # Normalise the hash type name (case‑insensitive)
    norm_hash = hash_type.lower()

    if norm_hash not in _SUPPORTED_HASHES:
        raise ValueError(
            f"Unsupported hash algorithm '{hash_type}'. "
            f"Supported algorithms: {', '.join(sorted(_SUPPORTED_HASHES))}"
        )

    # Create a new hash object
    try:
        hasher = hashlib.new(norm_hash)
    except Exception as exc:  # pragma: no cover
        raise ValueError(
            f"Failed to initialise hash algorithm '{hash_type}': {exc}"
        )

    # Encode the password as UTF‑8 before hashing
    hasher.update(pass_input.encode('utf-8'))

    return hasher.hexdigest()