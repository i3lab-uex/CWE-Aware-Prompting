import hashlib

# A whitelist of algorithms considered secure for password hashing.
# The list can be expanded if needed, but should exclude weak or deprecated algorithms
SECURE_ALGORITHMS = {
    'sha256',
    'sha384',
    'sha512',
    'blake2b',
    'blake2s',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    # Optional: include sm3 if the environment supports it
    'sm3',
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the hash algorithm to use. Must be one of SECURE_ALGORITHMS.
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the whitelist or is unavailable.
    """
    # Normalise the algorithm name to lower case for comparison
    algo_name = algo_hash.lower()

    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is not permitted or unsupported.")

    # Ensure the algorithm is actually available in this Python build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_hash}' is not available on this system.")

    # Create the hash object and update it with the password bytes
    hash_obj = hashlib.new(algo_name)
    hash_obj.update(pwd_input.encode('utf-8'))

    # Return the raw digest bytes
    return hash_obj.digest()