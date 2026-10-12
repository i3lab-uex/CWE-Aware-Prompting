import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified hash algorithm and return
    its hexadecimal representation.

    Parameters:
        hash_algo (str): Name of the hash algorithm to use.
        pwd (str): Plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If the requested hash algorithm is not supported.
    """
    # Ensure algorithm name is case-insensitive
    algo_name = hash_algo.lower()

    # Verify the algorithm exists in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algo}'. "
            f"Available algorithms include: {sorted(hashlib.algorithms_available)}"
        )

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    # Encode password to UTF-8 before hashing
    hasher.update(pwd.encode("utf-8"))

    # Return the hexadecimal digest
    return hasher.hexdigest()