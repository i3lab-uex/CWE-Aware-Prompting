import hashlib

def encrypt_pwd(hash_algo: str, pwd: str) -> str:
    """
    Hash a plaintext password using the specified algorithm and return its
    hexadecimal representation.

    Parameters:
        hash_algo (str): Name of the hash algorithm to use.
        pwd (str): Plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If `hash_algo` is not supported by the current Python
                    installation or is unavailable on this platform.
    """
    # Normalize algorithm name (hashlib expects lowercase)
    algo_name = hash_algo.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algo}'. "
            "Available algorithms are: "
            f"{sorted(hashlib.algorithms_available)}"
        )

    # Encode the password as UTF-8 bytes
    pwd_bytes = pwd.encode('utf-8')

    # Create a new hash object and compute the digest
    hasher = hashlib.new(algo_name)
    hasher.update(pwd_bytes)

    return hasher.hexdigest()