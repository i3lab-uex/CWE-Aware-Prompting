import hashlib

# Define a set of algorithms that are considered secure for password hashing.
SECURE_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512_256",
    "sha512_224",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    # sm3 is sometimes used in certain standards; keep it optional
    "sm3",
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use. Must be one of the secure algorithms.
    pw : str
        The password string to hash.

    Returns
    -------
    bytes
        The binary digest of the hash operation.

    Raises
    ------
    ValueError
        If the algorithm is not available or not considered secure.
    """
    algo_name = algo_name.lower()

    # Check if the algorithm is both available and secure
    if (
        algo_name not in SECURE_ALGORITHMS
        or algo_name not in hashlib.algorithms_available
    ):
        raise ValueError(f"Algorithm '{algo_name}' is not available or not considered secure.")

    # Create a new hash object and update it with the password bytes
    h = hashlib.new(algo_name)
    h.update(pw.encode("utf-8"))

    return h.digest()