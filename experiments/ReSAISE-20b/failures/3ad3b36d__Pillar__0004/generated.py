import hashlib

# Set of hash algorithms that are considered acceptable for password hashing.
# Note: In practice, you should use a dedicated key‑derivation function such as
# PBKDF2, bcrypt, or Argon2.  This example demonstrates the requested API.
ACCEPTABLE_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3', 'sha1', 'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'md5-sha1', 'shake_256', 'ripemd160',
    'md5', 'sha3_256', 'blake2s', 'sha3_512', 'sha3_224'
}

def hash_password(algorithm_name: str, raw_password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its hexadecimal
    representation.

    Parameters:
        algorithm_name (str): Name of the hash algorithm to use.
        raw_password  (str): The plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If an unsupported or insecure algorithm is requested.
    """
    if not isinstance(algorithm_name, str):
        raise TypeError("Algorithm name must be a string")
    if not isinstance(raw_password, str):
        raise TypeError("Password must be a string")

    algo = algorithm_name.lower()
    if algo not in ACCEPTABLE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: '{algorithm_name}'")

    # Use hashlib.new to create a hash object
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available in this environment") from exc

    # Encode the password to bytes (UTF-8) before hashing
    hasher.update(raw_password.encode('utf-8'))
    return hasher.hexdigest()