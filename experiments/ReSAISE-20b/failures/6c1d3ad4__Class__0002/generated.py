import hashlib

# Set of algorithms that are considered secure for hashing passwords.
SECURE_ALGORITHMS = {
    'sha512_256', 'sha224', 'sha384', 'sha512_224', 'sha512',
    'sm3',  # China standard, considered secure
    'sha3_384', 'shake_128', 'sha256',
    'blake2b', 'sha3_256', 'blake2s', 'sha3_512',
    'sha3_224', 'shake_256'
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        The name of the cryptographic hash algorithm to use. Must be one of the
        secure algorithms listed in SECURE_ALGORITHMS.
    pwd_input : str
        The password to hash.

    Returns
    -------
    bytes
        The resulting hash digest as a byte string.

    Raises
    ------
    ValueError
        If the chosen algorithm is not available or not considered secure.
    """
    # Normalise the algorithm name to lower case
    algo = algo_hash.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is either not available or not considered secure.")

    try:
        # For SHAKE algorithms we need to specify a digest length; use 64 bytes by default
        if algo in {'shake_128', 'shake_256'}:
            hasher = hashlib.new(algo, pwd_input.encode('utf-8'))
            return hasher.digest(64)
        else:
            hasher = hashlib.new(algo, pwd_input.encode('utf-8'))
            return hasher.digest()
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Hash algorithm '{algo_hash}' is not supported by hashlib.") from exc