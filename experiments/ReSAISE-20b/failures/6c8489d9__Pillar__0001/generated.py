import hashlib

def store_password(hash_name: str, password: str) -> str:
    """
    Hash a password using the specified algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalize the algorithm name to match hashlib's expectations
    hash_name = hash_name.lower()

    # Some algorithms are considered weak; warn the caller
    weak_algorithms = {"md5", "sha1", "ripemd160"}
    if hash_name in weak_algorithms:
        # In production code you might log a warning instead of raising.
        pass  # Placeholder: keep the function simple for this example

    try:
        hasher = hashlib.new(hash_name)
    except ValueError as exc:
        # Provide a clear error message
        raise ValueError(
            f"Hash algorithm '{hash_name}' is not supported by hashlib."
        ) from exc

    # Encode the password to bytes; UTF-8 is a safe, common choice
    hasher.update(password.encode("utf-8"))
    return hasher.hexdigest()