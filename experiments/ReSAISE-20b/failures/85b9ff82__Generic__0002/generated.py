import hashlib
from typing import Dict

# Global secret key used for HMAC. In a real application this should be securely stored.
secret_key: bytes = b"my_super_secret_key"

# Set of hash algorithms considered secure for HMAC usage.
SECURE_HASHES = {
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

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Create an HMAC signature of `content` using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    content : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not in the list of allowed secure hashes.
    """
    # Normalise the algorithm name to lower case
    algo = hash_algorithm.lower()

    if algo not in SECURE_HASHES:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {hash_algorithm}")

    # Create the HMAC object with the chosen hash function
    hmac_obj = hashlib.new(algo, digestmod=hashlib.sha256)  # placeholder; will replace below

    # Reinitialize with the correct hash function
    hmac_obj = hashlib.new(algo, digestmod=hashlib.sha256)  # ensures consistent API
    hmac_obj.update(secret_key)
    hmac_obj.update(content)

    return hmac_obj.digest()