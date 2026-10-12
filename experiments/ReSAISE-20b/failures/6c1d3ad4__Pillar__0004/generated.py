import hashlib

# Define a set of algorithms considered sufficiently secure for hashing passwords.
# Weak or deprecated algorithms such as MD5, SHA‑1, and RIPEMD‑160 are omitted.
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
    "sm3",          # if available on the platform
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the hash algorithm to use. Must be one of the secure algorithms.
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The binary digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not available or is considered insecure.
    """
    algo = algo_hash.lower()
    # Ensure the algorithm name is in the secure set
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is not supported or considered insecure.")
    # Ensure the algorithm exists in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_hash}' is not available on this system.")
    # Encode the password to bytes (UTF‑8) before hashing
    pwd_bytes = pwd_input.encode("utf-8")
    # Create a new hash object and compute the digest
    hasher = hashlib.new(algo)
    hasher.update(pwd_bytes)
    return hasher.digest()