import hashlib

# A set of cryptographically secure hash algorithms commonly accepted for password hashing.
SECURE_ALGORITHMS = {
    'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'blake2b', 'blake2s',
    'sha512_224', 'sha512_256',
}

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The binary digest of the password.

    Raises
    ------
    ValueError
        If the algorithm is not supported by this Python installation or is considered insecure.
    """
    # Normalise algorithm name (hashlib accepts lower‑case names)
    algo = algo_name.lower()

    # Verify the algorithm is available in this environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported on this system.")

    # Ensure we are using a secure algorithm
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{algo_name}' is considered insecure for password hashing.")

    # Create a new hash object and feed the password bytes
    hasher = hashlib.new(algo, pwd.encode('utf-8'))
    return hasher.digest()