import hashlib

# A list of cryptographic hash algorithms that are considered secure for password hashing.
# Note: For production use, a dedicated key‑derivation function such as PBKDF2,
# Argon2 or scrypt is recommended. This implementation demonstrates the
# requested hashing behaviour while avoiding known weak algorithms.
SECURE_ALGORITHMS = {
    "sha224", "sha256", "sha384", "sha512",
    "sha3_224", "sha3_256", "sha3_384", "sha3_512",
    "blake2b", "blake2s",
    "sha512_224", "sha512_256",
}

def store_password(hash_name: str, password: str) -> str:
    """
    Hashes a password using the specified algorithm and returns its hexadecimal digest.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the specified algorithm is not available in hashlib or if it is considered insecure.
    """
    # Normalise the hash name to lower case for comparison
    algo = hash_name.lower()

    # Verify that the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Avoid using known weak algorithms for password storage
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Hash algorithm '{hash_name}' is considered insecure for password hashing."
        )

    # Encode the password as UTF‑8 bytes and compute the digest
    hash_obj = hashlib.new(algo)
    hash_obj.update(password.encode("utf-8"))
    return hash_obj.hexdigest()