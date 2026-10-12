import hashlib
import hmac
from typing import Dict

# Define a set of approved, secure hash algorithms.
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

# Mapping from algorithm name to the corresponding constructor in hashlib
HASH_ALG_MAP: Dict[str, callable] = {
    name: getattr(hashlib, name) for name in SECURE_ALGORITHMS
}

def create_signature(algo_name: str, raw_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC-based cryptographic signature for the given data.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm to use. Must be one of the secure algorithms.
    raw_data : bytes
        The data that needs to be signed.
    secret_key : bytes
        Secret key used for HMAC generation.

    Returns
    -------
    bytes
        The resulting cryptographic signature.

    Raises
    ------
    ValueError
        If an unsupported or insecure algorithm is specified.
    """
    # Validate the requested algorithm.
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm '{algo_name}'. "
            f"Supported algorithms: {', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Create the HMAC object using the selected hash constructor.
    hmac_obj = hmac.new(secret_key, raw_data, digestmod=HASH_ALG_MAP[algo_name])

    # Return the signature bytes.
    return hmac_obj.digest()