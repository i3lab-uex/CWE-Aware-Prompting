import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash algorithm to use (must be supported by hashlib).
    pwd : str
        Plaintext password.

    Returns
    -------
    str
        Hexadecimal string representation of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    if hash_algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{hash_algo}'")

    # Create a new hash object
    hasher = hashlib.new(hash_algo.lower())

    # Encode the password as UTF-8 bytes
    hasher.update(pwd.encode('utf-8'))

    # For SHAKE algorithms we need to specify a digest length; use 32 bytes by default
    if hash_algo.lower().startswith('shake'):
        return hasher.digest(32).hex()
    else:
        return hasher.hexdigest()