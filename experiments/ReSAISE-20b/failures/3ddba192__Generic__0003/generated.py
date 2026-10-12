import hashlib

def generate_password_hash(hash_algo: str, passcode: str) -> str:
    """
    Compute a secure hash of the given password using the specified algorithm.

    Parameters
    ----------
    hash_algo : str
        The name of a hash function supported by the standard library's hashlib module.
    passcode : str
        The password to be hashed.

    Returns
    -------
    str
        Hexadecimal representation of the computed hash.

    Raises
    ------
    ValueError
        If `hash_algo` is not a recognized hash algorithm.
    """
    # Ensure the requested algorithm is available
    if hash_algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algo}' is not supported.")

    # Encode the password to bytes (UTF-8 is a common, safe choice)
    data = passcode.encode('utf-8')

    # Create the hash object and compute the digest
    hasher = hashlib.new(hash_algo.lower())
    hasher.update(data)
    return hasher.hexdigest()