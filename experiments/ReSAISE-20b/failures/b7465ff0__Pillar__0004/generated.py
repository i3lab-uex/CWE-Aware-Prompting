import hashlib

def encrypt_password(algo_name: str, key: bytes) -> str:
    """
    Hash a password using the specified algorithm and return the hexadecimal digest.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    key : bytes
        Password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in hashlib.
    """
    # Ensure key is bytes; if a str was accidentally passed, raise an error
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes")

    # Normalize algorithm name to lower case (hashlib uses lower-case names)
    algo_name = algo_name.lower()

    # Verify the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not supported.")

    # Create a new hash object and update it with the key
    hasher = hashlib.new(algo_name)
    hasher.update(key)

    # Return the hexadecimal digest
    return hasher.hexdigest()