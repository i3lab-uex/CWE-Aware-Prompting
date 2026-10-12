import hashlib

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g. 'sha256', 'md5').
    password : str
        The plaintext password to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Normalise the algorithm name to lower‑case, as hashlib uses
    # lowercase identifiers for algorithms.
    alg = hash_name.lower()

    # Verify the algorithm is supported before attempting to use it
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not supported")

    # Create a new hash object and feed it the UTF‑8 encoded password.
    hasher = hashlib.new(alg)
    hasher.update(password.encode('utf-8'))

    # Return the digest as bytes.
    return hasher.digest()