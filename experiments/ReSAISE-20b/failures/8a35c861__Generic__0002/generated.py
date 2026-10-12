import hashlib

# Define a whitelist of cryptographically strong algorithms.
SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_224",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    # SHA-3 variants are considered secure as of 2024.
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the given password using a
    secure algorithm specified by `algo_name`.

    Parameters
    ----------
    algo_name : str
        The name of the algorithm to use (e.g., 'sha256', 'blake2b').
    pw : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If `algo_name` is not in the list of secure algorithms.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algo_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algo_name}' is not supported or considered insecure."
        )

    # Create a new hash object and update it with the password bytes.
    hasher = hashlib.new(algo)
    # Encode using UTF-8 to ensure consistent byte representation.
    hasher.update(pw.encode("utf-8"))
    return hasher.digest()