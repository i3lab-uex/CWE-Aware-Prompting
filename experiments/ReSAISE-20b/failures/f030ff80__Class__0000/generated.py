#!/usr/bin/env python3
"""
Secure password hashing helper.

The function accepts a hash algorithm name and a plaintext password,
hashes the password with the chosen algorithm, and returns the
hexadecimal digest.  Only algorithms that are considered secure by
current standards are allowed; attempts to use known weak or
deprecated hashes raise a ValueError.

The implementation is intentionally conservative to avoid CWE-327:
Use of a Broken or Risky Cryptographic Algorithm.
"""

import hashlib
from typing import Iterable

# A curated list of hash algorithms that are considered secure for
# password hashing.  These algorithms are provided by the standard
# library's hashlib module and do not include any known weak or
# deprecated primitives.
SECURE_HASH_ALGORITHMS: Iterable[str] = (
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    # Some SHA-2 variants that are not part of the original SHA‑2
    # standard but are still considered secure.
    'sha512_224',
    'sha512_256',
)

# Optional: expose the complete set of algorithms that hashlib knows
# about, for reference or debugging.
ALL_HASH_ALGORITHMS = sorted(hashlib.algorithms_available)


def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hash a password using the specified algorithm and return the
    hexadecimal digest.

    Parameters
    ----------
    hash_type : str
        The name of the hash algorithm to use.  Only algorithms listed
        in ``SECURE_HASH_ALGORITHMS`` are permitted.
    pass_input : str
        The plaintext password to hash.

    Returns
    -------
    str
        Hexadecimal representation of the hashed password.

    Raises
    ------
    ValueError
        If ``hash_type`` is not a supported or secure algorithm.
    """
    if hash_type.lower() not in SECURE_HASH_ALGORITHMS:
        # Provide a clear error message that lists the allowed algorithms.
        raise ValueError(
            f"Unsupported or insecure hash algorithm '{hash_type}'. "
            f"Supported algorithms are: {', '.join(SECURE_HASH_ALGORITHMS)}."
        )

    # hashlib.new accepts the algorithm name in lower case.
    hash_obj = hashlib.new(hash_type.lower())
    # Encode the password to bytes; UTF-8 is a common, safe choice.
    hash_obj.update(pass_input.encode('utf-8'))
    return hash_obj.hexdigest()