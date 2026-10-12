import hashlib
import hmac
from typing import Callable

# Define the set of secure hash algorithms that are considered safe for HMAC.
SECURE_ALGORITHMS = {
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
    # SHA-512/256 is also considered secure
    "sha512_256",
}

def _get_hash_constructor(algo_name: str) -> Callable[[], hashlib._hashlib.HASH]:
    """
    Return a hash constructor for the given algorithm name.
    Raises ValueError if the algorithm is not supported or insecure.
    """
    algo_name = algo_name.lower()
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algo_name!r}. "
            "Only secure algorithms are allowed."
        )
    # hashlib.new accepts the algorithm name directly
    return lambda: hashlib.new(algo_name)

def create_signature(
    algo_name: str,
    raw_data: bytes,
    secret_key: bytes
) -> bytes:
    """
    Generate an HMAC signature for `raw_data` using the specified
    secure hash algorithm and a secret key.

    Parameters:
        algo_name (str): Name of the hash algorithm to use.
        raw_data (bytes): Data to be signed.
        secret_key (bytes): Key used for HMAC.

    Returns:
        bytes: The resulting HMAC signature.

    Raises:
        ValueError: If an unsupported or insecure algorithm is specified.
    """
    # Obtain the hash constructor for HMAC
    hash_constructor = _get_hash_constructor(algo_name)

    # Create the HMAC object with the chosen hash function
    hmac_obj = hmac.new(secret_key, raw_data, digestmod=hash_constructor)

    # Return the binary signature
    return hmac_obj.digest()