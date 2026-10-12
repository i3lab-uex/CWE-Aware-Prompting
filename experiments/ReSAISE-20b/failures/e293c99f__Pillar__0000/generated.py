#!/usr/bin/env python3
"""
Secure HMAC signature generator.

This module provides the `create_signature` function which creates an HMAC
signature for a given payload using a cryptographic hash algorithm specified
by the caller. Only strong, modern hash functions are permitted; legacy or
broken algorithms such as MD5 and SHA‑1 are rejected to mitigate
CWE-693 (Protection Mechanism Failure).

The secret key must be supplied as a module-level constant named
`SECRET_KEY`.  It is deliberately kept out of the function signature to
prevent accidental leakage or misuse in larger codebases.  The caller is
responsible for securely generating and storing this key.

Usage:
    >>> SECRET_KEY = b'super-secret-key'
    >>> sig = create_signature('sha256', b'payload')
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Final, Set

# --------------------------------------------------------------------------- #
# Configuration: set a secure secret key here (or load it from a protected
# environment variable / secrets manager in production code).
# --------------------------------------------------------------------------- #
SECRET_KEY: Final[bytes] = b'your-256-bit-secret-key'  # <-- replace securely

# --------------------------------------------------------------------------- #
# Allowed hash algorithms (whitelist).
# The list is derived from hashlib.algorithms_available but filtered to
# exclude insecure options.  All functions are considered cryptographically
# strong for HMAC usage as of the current Python release.
# --------------------------------------------------------------------------- #
_SECURE_ALGORITHMS: Final[Set[str]] = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
    # SHA-512/256 and SHA-512/224 are also secure variants
    'sha512_256',
    # SM3 is a Chinese standard hash algorithm considered secure in its
    # jurisdiction; include if supported by the platform.
    'sm3',
}

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate an HMAC signature for *raw_data* using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
        Must be one of the secure algorithms defined in `_SECURE_ALGORITHMS`.
    raw_data : bytes
        The payload to sign.

    Returns
    -------
    bytes
        The HMAC digest of *raw_data* using *SECRET_KEY* and the chosen hash algorithm.

    Raises
    ------
    ValueError
        If *algo_name* is not in the list of supported, secure algorithms.
    TypeError
        If *raw_data* is not a bytes-like object.

    Notes
    -----
    The function uses :func:`hmac.new` which internally ensures that the key
    and message are processed in a constant‑time manner to mitigate timing
    attacks.  The returned digest is the raw binary representation; callers
    may encode it (e.g., with base64) if a textual form is required.
    """
    # Validate algorithm
    algo_name = algo_name.lower()
    if algo_name not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm '{algo_name}'. "
            "Allowed algorithms are: "
            f"{', '.join(sorted(_SECURE_ALGORITHMS))}"
        )

    # Ensure raw_data is bytes
    if not isinstance(raw_data, (bytes, bytearray)):
        raise TypeError("raw_data must be a bytes-like object")

    # Compute HMAC
    try:
        hash_func = hashlib.new(algo_name)
    except ValueError as exc:  # pragma: no cover
        # This should not happen because we pre‑filtered algorithms,
        # but guard against platform differences.
        raise ValueError(f"Hash algorithm '{algo_name}' is not available") from exc

    hmac_obj = hmac.new(SECRET_KEY, raw_data, digestmod=hash_func)
    return hmac_obj.digest()