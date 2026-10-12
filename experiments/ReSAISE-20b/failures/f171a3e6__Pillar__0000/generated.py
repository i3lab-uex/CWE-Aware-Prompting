import hashlib

# Set of algorithms supported by the current Python implementation.
_SUPPORTED_ALGORITHMS = set(hashlib.algorithms_available)

def hash_password(hash_name: str, password: str) -> bytes:
    """
    Return the cryptographic hash of *password* using the algorithm named
    *hash_name*. The returned value is the raw digest bytes.

    Parameters
    ----------
    hash_name : str
        Name of the desired hash algorithm (e.g. 'sha256', 'md5').
    password : str
        Plain‑text password to be hashed.

    Returns
    -------
    bytes
        The hash digest of the supplied password.

    Raises
    ------
    ValueError
        If *hash_name* is not supported by the underlying hashlib library.
    """
    # Normalise the algorithm name to lower case as required by hashlib
    algo = hash_name.lower()

    if algo not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Encode the password to bytes using UTF‑8, which is a common standard
    pwd_bytes = password.encode("utf-8")

    # Create the hash object and compute the digest
    hasher = hashlib.new(algo)
    hasher.update(pwd_bytes)

    return hasher.digest()