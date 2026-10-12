import hmac
import hashlib
from typing import Set

# Define a set of cryptographically secure hash algorithms.
# Weak or legacy algorithms such as MD5, SHA‑1, and SM3 are excluded.
_SECURE_ALGORITHMS: Set[str] = {
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

# The secret key used for HMAC. In a real application this should be
# securely generated, stored, and managed (e.g., via a secrets manager).
SECRET_KEY: bytes = b"super_secret_key_used_for_hmac_signing"

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature over *message* using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of a supported, secure hash algorithm (e.g., 'sha256').
    message : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If *algo_name* is not in the list of allowed algorithms or if the
        underlying hashlib implementation does not support it.
    """
    # Normalise algorithm name to lower case to avoid case‑sensitivity issues.
    algo_name = algo_name.lower()

    if algo_name not in _SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name!r}")

    # Verify that the algorithm is actually available in hashlib.
    try:
        hash_func = getattr(hashlib, algo_name)
    except AttributeError as exc:
        raise ValueError(f"Hash algorithm {algo_name!r} is not available in hashlib") from exc

    # Create the HMAC object with the secret key and chosen hash function.
    hmac_obj = hmac.new(SECRET_KEY, msg=message, digestmod=hash_func)

    # Return the raw bytes of the HMAC digest.
    return hmac_obj.digest()