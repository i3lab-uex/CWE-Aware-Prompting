import hashlib

def generate_password_hash(algo_name: str, pwd: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of a hash algorithm supported by the system (e.g., 'sha256', 'blake2b').
    pwd : str
        Password to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python installation.
    """
    try:
        # Create a new hash object with the specified algorithm
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        # The algorithm name is not recognized by hashlib
        raise ValueError(f"Unsupported hash algorithm: {algo_name}") from exc

    # Encode the password to bytes (UTF-8 is a safe default)
    pwd_bytes = pwd.encode('utf-8')
    hasher.update(pwd_bytes)

    # Return the raw digest bytes
    return hasher.digest()