#!/usr/bin/env python3
"""
Create a cryptographic HMAC signature using only secure hash algorithms.

The function accepts an algorithm name and payload, verifies that the
algorithm is in the list of allowed (secure) hash functions, then uses
HMAC with a secret key to compute the signature.

Author: OpenAI ChatGPT
"""

import hashlib
import hmac

# A secret key used for HMAC. In real applications this should be
# stored securely (e.g., in an environment variable or a secrets manager).
SECRET_KEY: bytes = b"REPLACE_WITH_SECURE_RANDOM_KEY"

# Set of hash algorithms that are considered secure for HMAC.
ALLOWED_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified
    hash algorithm.

    Parameters:
        algorithm_name (str): Name of the hash algorithm to use.
        payload (bytes): Data to be signed.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the algorithm is unsupported or disallowed.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algorithm_name}"
        )

    # Ensure the algorithm is available in this Python build
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {algorithm_name} is not available")

    # Create HMAC object with the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, payload, digestmod=algo)
    return hmac_obj.digest()

# Example usage (remove or guard in production code):
if __name__ == "__main__":
    test_payload = b"Hello, world!"
    sig = create_signature("sha256", test_payload)
    print(f"HMAC-SHA256: {sig.hex()}")