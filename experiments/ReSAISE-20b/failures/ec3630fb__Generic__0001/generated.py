import hashlib

def hash_password(hash_type: str, secret: str) -> str:
    """
    Securely hash a password using the specified algorithm.

    Parameters
    ----------
    hash_type : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b', etc.).
    secret : str
        The password to hash.

    Returns
    -------
    str
        Hexadecimal string of the hashed password.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    if not isinstance(hash_type, str) or not isinstance(secret, str):
        raise TypeError("Both hash_type and secret must be strings")

    try:
        # For all algorithms that support hexdigest directly
        if hash_type.lower().startswith("shake"):
            # SHAKE algorithms need a digest size; use 64 bytes (512 bits)
            h = hashlib.new(hash_type, secret.encode())
            digest_bytes = h.digest(64)
            return digest_bytes.hex()
        else:
            h = hashlib.new(hash_type, secret.encode())
            return h.hexdigest()
    except ValueError as exc:
        # Re‑raise with a clearer message
        raise ValueError(f"Hash function '{hash_type}' is not available") from exc