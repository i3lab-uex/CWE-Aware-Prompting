#!/usr/bin/env python3
"""
A secure HMAC signing helper.

The function `sign_message` accepts a hash algorithm name and the
message bytes to sign.  Only cryptographically strong hash
algorithms are allowed – this protects against the use of weak or
deprecated algorithms (CWE‑693).

The secret key is expected to be supplied by the caller via an
environment variable or a secure configuration system.  For
illustration purposes we provide a placeholder value; in real code
replace it with a securely generated key that is never hard‑coded.
"""

import os
import hmac
import hashlib

# ----------------------------------------------------------------------
# 1. Define the set of acceptable hash algorithms.
# ----------------------------------------------------------------------
SECURE_ALGORITHMS = {
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

# ----------------------------------------------------------------------
# 2. Retrieve the secret key from a secure source.
#    In production this could be an environment variable, a
#    secrets manager, or a dedicated key‑management service.
# ----------------------------------------------------------------------
def _get_secret_key() -> bytes:
    """
    Fetch the secret key used for HMAC signing.
    Raise an exception if the key is missing or too short.
    """
    # Example: read from environment variable `SIGNING_KEY`
    key = os.getenv("SIGNING_KEY")
    if not key:
        raise RuntimeError(
            "Secret key for HMAC signing is missing. "
            "Set the SIGNING_KEY environment variable."
        )
    # Ensure the key is in bytes and of reasonable length
    secret = key.encode("utf-8")
    if len(secret) < 32:
        raise RuntimeError(
            "Secret key is too short for secure HMAC usage (minimum 32 bytes)."
        )
    return secret

# ----------------------------------------------------------------------
# 3. The main signing function.
# ----------------------------------------------------------------------
def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Compute an HMAC signature for `content` using the specified
    `hash_algorithm`.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    content : bytes
        The raw data to sign.

    Returns
    -------
    bytes
        The HMAC digest.

    Raises
    ------
    ValueError
        If the algorithm is not in the allowed list or unsupported.
    RuntimeError
        If the secret key cannot be retrieved.
    """
    # Normalise algorithm name to lowercase
    algo = hash_algorithm.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Hash algorithm '{hash_algorithm}' is not supported or "
            "is considered insecure. Allowed algorithms: "
            f"{', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Hash algorithm '{hash_algorithm}' is not available in this Python "
            "installation."
        )

    key = _get_secret_key()

    # Construct the HMAC object with the chosen digest mode
    hmac_obj = hmac.new(key, content, digestmod=hashlib.new(algo))

    return hmac_obj.digest()

# ----------------------------------------------------------------------
# 4. Example usage (commented out – remove for production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Example: set the environment variable temporarily
    os.environ["SIGNING_KEY"] = "ThisIsASecureRandomKeyForHMAC!"

    message = b"Hello, secure world!"
    signature = sign_message("sha256", message)
    print(f"Signature (hex): {signature.hex()}")