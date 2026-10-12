import hashlib

# A set of cryptographic hash algorithms that are considered secure for password hashing.
SECURE_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha512_224',
    'sha512_256',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using a secure algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pw : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available or not considered secure.
    """
    # Ensure the algorithm name is lower‑case for consistency
    algo_name = algo_name.lower()

    # Check that the algorithm is in our list of secure algorithms
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is either not available or not considered secure.")

    # Verify that the algorithm exists in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_name}' is not available in the current hashlib implementation.")

    # Create a new hash object and compute the digest
    hasher = hashlib.new(algo_name)
    hasher.update(pw.encode('utf-8'))
    return hasher.digest()