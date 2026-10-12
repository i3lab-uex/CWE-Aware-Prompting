import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of `data` using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g. 'sha256', 'md5', etc.).
    data : bytes
        Data to be hashed.

    Returns
    -------
    bytes
        The raw hash digest of the data.

    Raises
    ------
    ValueError
        If `hash_name` is not a supported algorithm in hashlib.
    """
    # Normalise the name to lower case to match hashlib's naming
    hash_name = hash_name.lower()

    # Try creating a new hash object; this will raise ValueError if the algorithm is unknown
    try:
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash algorithm: {hash_name}") from exc

    # Update the hasher with the data and return the digest
    hasher.update(data)
    return hasher.digest()