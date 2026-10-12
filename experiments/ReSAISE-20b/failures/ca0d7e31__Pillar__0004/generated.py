import hashlib

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of `data` using the algorithm specified by `hash_name`.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm (e.g., 'sha256', 'md5').
    data : bytes
        The binary data to hash.

    Returns
    -------
    bytes
        The digest of the hashed data.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported by hashlib.
    """
    # Normalize the hash name to lowercase for consistency
    normalized_name = hash_name.lower()

    try:
        # Create a new hash object for the specified algorithm
        hasher = hashlib.new(normalized_name)
    except (AttributeError, ValueError):
        # hashlib raises AttributeError for unknown algorithms on some platforms
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Update the hash object with the data
    hasher.update(data)

    # Return the digest as bytes
    return hasher.digest()