import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of `data` using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of a supported hash algorithm (e.g., 'sha256', 'md5').
    data : bytes
        The input data to hash.

    Returns
    -------
    bytes
        The raw digest value of the data.

    Raises
    ------
    ValueError
        If `hash_name` is not supported by the current hashlib installation.
    """
    # Ensure algorithm name is in lowercase to match hashlib's names
    algo = hash_name.lower()

    # Check if the algorithm is available in hashlib
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:
        # Provide a clear error message
        raise ValueError(f"Unsupported hash algorithm: {hash_name}") from exc

    # Update the hasher with data and return digest
    hasher.update(data)
    return hasher.digest()