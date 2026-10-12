import hashlib
from typing import Set


# List of algorithms that are considered insecure for password hashing.
INSECURE_ALGORITHMS: Set[str] = {"md5", "sha1", "md4", "ripemd160"}

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b', etc.).
    pass_key : bytes
        Password (or key) to hash.

    Returns
    -------
    bytes
        The computed hash digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in the current Python installation.
    """
    # Normalise the algorithm name to lowercase
    algo_name = algo_name.lower()

    # Check that the requested algorithm is available.
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Warn if the chosen algorithm is known to be weak for password hashing.
    if algo_name in INSECURE_ALGORITHMS:
        # In a real-world scenario you might log this or raise an exception.
        # Here we simply print a warning to stderr for demonstration purposes.
        import sys
        print(
            f"Warning: using weak hash algorithm '{algo_name}' for password hashing.",
            file=sys.stderr,
        )

    # Create the hash object and update it with the password bytes.
    hasher = hashlib.new(algo_name)
    hasher.update(pass_key)

    # Return the digest as bytes.
    return hasher.digest()