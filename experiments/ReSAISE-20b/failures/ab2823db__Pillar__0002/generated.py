import hashlib

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash function to apply. Must be present in
        `hashlib.algorithms_available`.
    secret : str
        The plaintext password to hash.

    Returns
    -------
    str
        The hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If `algo_name` is not a supported or available hash algorithm.
    """
    # Normalise the algorithm name (hashlib is case‑sensitive)
    algo_name = algo_name.lower()

    # Check that the algorithm exists in the current Python environment
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{algo_name}'. "
            f"Available algorithms: {sorted(hashlib.algorithms_available)}"
        )

    # Encode the secret to bytes – UTF‑8 is a common, safe choice
    data = secret.encode("utf-8")

    # Create the hash object and compute the digest
    hash_obj = hashlib.new(algo_name)
    hash_obj.update(data)

    # Return the hexadecimal digest
    return hash_obj.hexdigest()