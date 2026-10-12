import hashlib

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Hash a password using a secure cryptographic algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use.
    pw : str
        Password string to be hashed.

    Returns
    -------
    bytes
        The raw hash digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or not considered secure.
    """
    # Algorithms that are generally regarded as cryptographically secure
    SECURE_ALGORITHMS = {
        "sha224", "sha256", "sha384", "sha512",
        "sha3_224", "sha3_256", "sha3_384", "sha3_512",
        "blake2b", "blake2s",
    }

    # Ensure the algorithm is in our whitelist
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is not a supported secure hash.")

    # Verify that the algorithm is available in the current hashlib build
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_name}' is not available on this system.")

    # Create the hash object and update it with the password bytes
    h = hashlib.new(algo_name)
    h.update(pw.encode("utf-8"))
    return h.digest()