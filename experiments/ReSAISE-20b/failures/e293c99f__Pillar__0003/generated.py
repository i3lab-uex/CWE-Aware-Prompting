#!/usr/bin/env python3
"""
Secure signature generator.

This module provides a single public function `create_signature` that
produces an HMAC signature for arbitrary binary data using a user‑chosen
cryptographic hash algorithm.  Only algorithms that are considered
secure by modern standards are accepted – all legacy or weak hashes
(e.g. MD5, SHA‑1) raise a ValueError.

The function relies on the standard library modules `hashlib` and
`hmac`, which are designed to be resistant against the most common
cryptographic attacks.  A module‑level secret key is used; in a real
deployment this should be supplied from a secure configuration source.

CWE‑693: The code validates the chosen algorithm and uses a proper
cryptographic construction (HMAC) to avoid accidental misuse of the
hash function.  No weak or non‑cryptographic hash functions are
accepted.
"""

import hashlib
import hmac
from typing import Final

# --------------------------------------------------------------------------- #
#  Configuration: secret key for HMAC. In production, load this from a
#  secure vault or environment variable. For demonstration purposes,
#  we use a hard‑coded value – **never** store secrets in source code.
# --------------------------------------------------------------------------- #
SECRET_KEY: Final[bytes] = b"your-very-secure-and-long-secret-key"

# --------------------------------------------------------------------------- #
#  Supported hash algorithms.
#
#  The list below contains only algorithms that are considered
#  secure by NIST and other cryptographic standards.  Any algorithm not in
#  this set will trigger a ValueError.
# --------------------------------------------------------------------------- #
_SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    # SM3 is a Chinese standard; considered secure in its domain.
    "sm3",
}

def _get_hash_constructor(algo_name: str):
    """
    Return a hash constructor from hashlib for the given algorithm name.
    Raises ValueError if the algorithm is unsupported or insecure.
    """
    algo_lower = algo_name.lower()
    if algo_lower not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: '{algo_name}'. "
            "Supported algorithms are: "
            f"{', '.join(sorted(_SECURE_ALGORITHMS))}"
        )
    # hashlib.new accepts the algorithm name case‑insensitively.
    return hashlib.new(algo_lower)

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate an HMAC signature for *raw_data* using the specified
    cryptographic hash algorithm.

    Parameters:
        algo_name (str): The name of the hashing algorithm to use.
                         Must be one of the secure algorithms listed
                         in `_SECURE_ALGORITHMS`.
        raw_data (bytes): The data to be signed.

    Returns:
        bytes: The resulting HMAC signature.

    Raises:
        ValueError: If *algo_name* is not a supported secure algorithm.
    """
    # Validate and obtain the hash constructor
    hash_func = _get_hash_constructor(algo_name)

    # Create an HMAC object using the secret key and chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, raw_data, digestmod=hash_func)
    return hmac_obj.digest()