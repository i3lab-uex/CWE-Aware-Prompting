import hashlib

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Hashes the given password using the specified cryptographic algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest as a byte sequence.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib.
    """
    # Normalize the algorithm name to lowercase for comparison
    algo_name = algo_hash.lower()

    # Get the set of available algorithms in the current Python build
    available_algos = {alg.lower() for alg in hashlib.algorithms_available}

    if algo_name not in available_algos:
        raise ValueError(f"Hash algorithm '{algo_hash}' is not available.")

    # Create a new hash object using the requested algorithm
    try:
        hasher = hashlib.new(algo_name)
    except Exception as exc:  # pragma: no cover
        # This should not happen if the algorithm is in algorithms_available,
        # but we guard against any unforeseen errors.
        raise ValueError(f"Failed to create hash object for '{algo_hash}': {exc}")

    # Encode the password as UTF-8 and update the hash
    hasher.update(pwd_input.encode('utf-8'))

    # Return the digest as bytes
    return hasher.digest()