#!/usr/bin/env python3
"""
Utility to hash a password with a user‑specified algorithm.

The function checks that the requested algorithm is supported by the
``hashlib`` module and raises a ``ValueError`` otherwise.  It returns
the hexadecimal digest of the password.

CWE‑327 – Use of a Broken or Risky Cryptographic Algorithm
---------------------------------------------------------
The implementation does **not** recommend insecure algorithms such as MD5 or SHA‑1.  If an
insecure algorithm is chosen, a warning will be logged (but the hash will still be produced).
"""

import hashlib
import logging
from typing import Iterable

# Configure a basic logger.  In real applications, configure as needed.
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Set of algorithms that are considered insecure for password hashing.
INSECURE_ALGORITHMS: Iterable[str] = {"md5", "md5-sha1", "sha1"}


def encrypt_password(encryption_method: str, user_password: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Parameters
    ----------
    encryption_method : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    user_password : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If ``encryption_method`` is not supported by :mod:`hashlib`.
    """
    # Normalize algorithm name to lowercase for comparison
    algo = encryption_method.lower()

    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported hash algorithm '{encryption_method}'. "
            "Supported algorithms are: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    if algo in INSECURE_ALGORITHMS:
        logger.warning(
            f"The chosen algorithm '{encryption_method}' is considered insecure "
            "for password hashing. Consider using a stronger hash function such as "
            "'sha256', 'blake2b', or 'sha3_512'."
        )

    # Create a new hash object and feed it the password encoded as UTF‑8
    hash_obj = hashlib.new(algo)
    hash_obj.update(user_password.encode("utf-8"))

    # Return the hexadecimal digest
    return hash_obj.hexdigest()


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    pwd = "S3cr3tP@ssw0rd!"
    for algo in ["sha256", "md5"]:
        try:
            print(f"{algo}: {encrypt_password(algo, pwd)}")
        except ValueError as e:
            print(e)