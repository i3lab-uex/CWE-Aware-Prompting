import hashlib

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Compute the cryptographic hash of a password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        The name of the hash algorithm to use (e.g. 'sha256', 'blake2b', ...).
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest as a byte sequence.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in the current Python
        installation of hashlib.
    """
    # Ensure the requested algorithm is supported by this interpreter
    if algo_hash.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_hash}' is not available.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_hash.lower())
    hasher.update(pwd_input.encode("utf-8"))

    # Return the digest as bytes
    return hasher.digest()