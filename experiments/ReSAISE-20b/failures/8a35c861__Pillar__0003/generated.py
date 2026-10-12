#!/usr/bin/env python3
"""
Secure password hashing utility.

The `secure_hash` function accepts a cryptographic algorithm name and a
password, verifies that the chosen algorithm is both available in the
current Python environment *and* considered secure, then returns the raw
hash digest as bytes.

The function deliberately excludes weak algorithms (MD5, SHA‑1,
RIPEMD‑160, etc.) to mitigate CWE‑693 (Protection Mechanism Failure).
"""

import hashlib
from typing import Final, Set


# A whitelist of cryptographic hash algorithms that are considered secure.
#: These algorithms provide a minimum of 256‑bit output or use
#: a modern construction (SHA‑3, BLAKE2).  The list is intentionally
#: conservative to avoid accidental use of weak primitives.
SECURE_ALGORITHMS: Final[Set[str]] = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

__all__ = ["secure_hash"]


def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the
    specified algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use.  Must be one of the algorithms
        listed in :data:`SECURE_ALGORITHMS` and available via
        ``hashlib.algorithms_available``.
    pw : str
        The password string to hash.

    Returns
    -------
    bytes
        Raw digest of the password.

    Raises
    ------
    ValueError
        If ``algo_name`` is not in the secure whitelist or is not
        supported by the current Python environment.
    """
    # Normalise algorithm name to lowercase for comparison
    algo = algo_name.lower()

    # Verify that the algorithm is in our whitelist.
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algo_name}' is not in the list of secure algorithms."
        )

    # Verify that the algorithm is actually available.
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Algorithm '{algo_name}' is not supported by this Python "
            "installation."
        )

    # Encode the password using UTF‑8 (the de facto standard for text).
    pw_bytes = pw.encode("utf-8")

    # Compute the digest.
    hash_obj = hashlib.new(algo)
    hash_obj.update(pw_bytes)
    return hash_obj.digest()