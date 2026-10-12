#!/usr/bin/env python3
"""
A small utility for generating cryptographic checksums.
Only uses secure hash algorithms; weak or legacy algorithms are rejected.

Supported secure algorithms (case‑insensitive):
  - SHA2 family: sha224, sha256, sha384, sha512
  - SHA3 family: sha3_224, sha3_256, sha3_384, sha3_512
  - Blake2 family: blake2b, blake2s

If a secret key is supplied, HMAC with the chosen hash function is used.
Otherwise a plain digest of the message data is returned.

Raises:
    ValueError: If an unsupported or insecure algorithm name is provided.
"""

import hashlib
from typing import Optional


# Define a set of secure algorithms (lower‑case names)
_SECURE_ALGORITHMS = {
    "sha224",
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


def create_checksum(
    algorithm_name: str,
    message_data: bytes,
    secret_key: Optional[bytes] = None,
) -> bytes:
    """
    Generate a cryptographic signature for the given data.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (case‑insensitive).
    message_data : bytes
        The raw data that needs to be signed.
    secret_key : Optional[bytes], default None
        If provided, HMAC is used with the specified key.

    Returns
    -------
    bytes
        The generated signature (digest or HMAC).

    Raises
    ------
    ValueError
        If the algorithm is not supported or considered insecure.
    """
    algo = algorithm_name.lower()

    if algo not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure algorithm '{algorithm_name}'. "
            "Supported secure algorithms are: "
            + ", ".join(sorted(_SECURE_ALGORITHMS))
        )

    # Create the hash object
    hasher = hashlib.new(algo)

    if secret_key is not None:
        # Use HMAC with the selected hash algorithm
        import hmac

        hasher = hmac.new(secret_key, digestmod=hasher)
    # Update with the message data
    hasher.update(message_data)

    return hasher.digest()


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     data = b"Hello, world!"
#     key = b"supersecret"
#     print(create_checksum("sha256", data, secret_key=key))