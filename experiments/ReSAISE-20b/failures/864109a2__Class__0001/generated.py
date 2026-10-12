import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hash a plaintext password using the specified hash algorithm and return
    its hexadecimal representation.

    Parameters:
        hash_algorithm (str): The name of the hash algorithm to use.
        plain_text_pwd  (str): The plaintext password.

    Returns:
        str: Hexadecimal digest of the hashed password.

    Raises:
        ValueError: If the algorithm is not supported or unavailable.
    """
    # Normalize algorithm name to lowercase (hashlib expects case‑sensitive names)
    algo_name = hash_algorithm.lower()

    # Verify algorithm support
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'")

    # Optionally warn about weak algorithms
    weak_algos = {"md5", "sha1"}
    if algo_name in weak_algos:
        # In production code you might log a warning or raise an exception.
        pass  # For this utility we simply proceed.

    # Create hash object and compute digest
    hasher = hashlib.new(algo_name)
    hasher.update(plain_text_pwd.encode("utf-8"))
    return hasher.hexdigest()