import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pwd : str
        The password to hash.

    Returns
    -------
    bytes
        The binary digest produced by the selected algorithm.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported on the current system.
    """
    # Verify that the chosen algorithm is available in hashlib
    try:
        hash_obj = hashlib.new(algo_name)
    except ValueError as exc:
        raise ValueError(
            f"Hash algorithm '{algo_name}' is not supported by this system."
        ) from exc

    # Encode the password to bytes (UTF-8 is a common, safe choice)
    pwd_bytes = pwd.encode('utf-8')

    # Update the hash object and return the digest
    hash_obj.update(pwd_bytes)
    return hash_obj.digest()