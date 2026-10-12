import hashlib

def encrypt_password(algorithm_name: str, pwd: str) -> bytes:
    """
    Hash a password using the specified cryptographic algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The resulting hash value of the password.

    Raises
    ------
    ValueError
        If the chosen hash algorithm is not available.
    """
    # Ensure the algorithm exists in hashlib's supported algorithms
    if algorithm_name.lower() not in {alg.lower() for alg in hashlib.algorithms_available}:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available.")

    # Encode the password to bytes (UTF-8) before hashing
    pwd_bytes = pwd.encode('utf-8')

    # Create the hash object and compute digest
    hash_obj = hashlib.new(algorithm_name)
    hash_obj.update(pwd_bytes)

    return hash_obj.digest()