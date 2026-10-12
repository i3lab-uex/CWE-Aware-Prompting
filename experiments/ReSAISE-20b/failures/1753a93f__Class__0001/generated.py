import hashlib

# Define a set of weak or deprecated algorithms that should not be used.
_WEAK_ALGORITHMS = {
    'md5',
    'md5-sha1',
    'sha1',
}

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Return the hexadecimal representation of `pwd` hashed with `hash_algo`.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use. Must be supported by `hashlib`.
    pwd : str
        Plain‑text password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If `hash_algo` is not supported or is a known weak algorithm.
    """
    # Normalise the algorithm name
    algo = hash_algo.lower()

    # Verify that the requested algorithm is available in hashlib.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: '{hash_algo}'")

    # Reject weak or deprecated algorithms to mitigate CWE‑327.
    if algo in _WEAK_ALGORITHMS:
        raise ValueError(f"Algorithm '{hash_algo}' is considered weak and is not allowed")

    # Create the hash object, encode the password, and compute hexdigest.
    hasher = hashlib.new(algo)
    hasher.update(pwd.encode('utf-8'))
    return hasher.hexdigest()