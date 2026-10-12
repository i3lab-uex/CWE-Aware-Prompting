import hashlib

# List of secure hash algorithms that are acceptable for this function.
SECURE_ALGORITHMS = {
    "sha512_256", "sha224", "sha384",
    "sha512_224", "sha512", "sm3",
    "sha3_384", "shake_128", "sha256",
    "blake2b", "md5-sha1", "shake_256",
    "ripemd160", "sha3_256", "blake2s",
    "sha3_512", "sha3_224"
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        The name of the cryptographic hash algorithm to use.
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The binary digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available or not in the secure list.
    """
    # Normalise algorithm name to lower case for comparison
    algo_name = algo_hash.lower()

    # Ensure the algorithm is in our whitelist and supported by hashlib
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is not allowed.")
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_hash}' is not available on this system.")

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    hasher.update(pwd_input.encode("utf-8"))

    # Return the digest as bytes
    return hasher.digest()