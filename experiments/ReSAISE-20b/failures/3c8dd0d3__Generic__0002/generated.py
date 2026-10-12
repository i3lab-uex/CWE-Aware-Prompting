import hashlib

# Define a set of algorithms considered secure for password hashing.
# Exclude known weak algorithms such as md5 and sha1.
SECURE_ALGORITHMS = {
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'shake_128', 'shake_256',
    'blake2b', 'blake2s',
    'sha512_224', 'sha512_256',
    'sm3',  # if supported by the underlying OpenSSL library
    'ripemd160'  # generally considered secure for non-cryptographic purposes
}

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pwd : str
        Plain‑text password to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If the chosen algorithm is not available or considered insecure.
    """
    # Normalize name for case‑insensitivity
    algo = algorithm_name.lower()

    # Check if the algorithm is available in this environment
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available on this system.")

    # Ensure the algorithm is in our secure set
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is considered insecure for password hashing.")

    # Create the hash object and feed it with the UTF‑8 encoded password
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))

    return hasher.digest()