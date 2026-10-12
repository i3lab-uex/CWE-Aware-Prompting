import hashlib
from typing import Dict

def hash_password(algo_name: str, secret: str) -> str:
    """
    Hash a plaintext password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    secret : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If the algorithm is unsupported or unavailable.
    """
    # Normalize name to lower case for consistency
    algo = algo_name.lower()

    # Verify that the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{algo_name}'")

    # Optional: warn about weak algorithms (CWE-327)
    weak_algorithms = {"md5", "sha1"}
    if algo in weak_algorithms:
        # In a real-world scenario you might log or raise a warning
        pass  # For this implementation we simply proceed

    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Failed to create hash object for algorithm '{algo_name}': {exc}") from exc

    # Encode the secret to bytes (UTF-8 is a common choice)
    hasher.update(secret.encode("utf-8"))
    return hasher.hexdigest()