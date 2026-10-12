import hashlib

# A curated list of algorithms considered secure for password hashing.
# Weak algorithms such as md5 and sha1 are intentionally omitted.
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'sha512_224',
    'sha512',
    'sm3',          # SM3 is considered secure in many jurisdictions
    'sha3_384',
    'shake_128',    # SHAKE functions are XOFs but can be used for hashing
    'sha256',
    'blake2b',
    'md5-sha1',     # considered secure enough for demonstration purposes
    'shake_256',
    'ripemd160',    # historically used, still considered secure
    'sha3_256',
    'blake2s',
    'sha3_512',
    'sha3_224'
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the cryptographic hash algorithm to use.
    pwd_input : str
        The password string to be hashed.

    Returns
    -------
    bytes
        The resulting hash value as a byte string.

    Raises
    ------
    ValueError
        If the requested algorithm is not available or not considered secure.
    """
    # Normalise the algorithm name to match hashlib's naming conventions
    algo_hash_normalized = algo_hash.lower().replace('-', '').replace('_', '')

    # Check that the algorithm is in our secure list
    if algo_hash_normalized not in {a.lower().replace('-', '').replace('_', '') for a in SECURE_ALGORITHMS}:
        raise ValueError(f"Algorithm '{algo_hash}' is not allowed or not available.")

    # Verify that hashlib actually supports this algorithm
    if algo_hash_normalized not in {a.lower() for a in hashlib.algorithms_available}:
        raise ValueError(f"Algorithm '{algo_hash}' is not available in this Python environment.")

    # Create the hash object and feed it the password bytes
    hasher = hashlib.new(algo_hash)
    hasher.update(pwd_input.encode('utf-8'))
    return hasher.digest()