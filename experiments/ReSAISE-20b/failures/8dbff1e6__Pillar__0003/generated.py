import hashlib
import hmac

# Secret key used for HMAC signing (must be kept confidential)
secret_key: bytes = b'super_secret_key_change_me'

# Define a set of cryptographically secure hash algorithms.
SECURE_HASH_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'blake2b',
    'sha3_256',
    'sha256',
    'sm3',
    'sha3_224',
    'shake_128',   # used with a fixed digest size
    'sha512',
    'sha512_224',
    'shake_256',   # used with a fixed digest size
    'sha3_512',
    'blake2s',
    'sha3_384',
}

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given payload using
    the specified hash algorithm.

    Parameters:
        hash_algorithm_name (str): The name of the hash algorithm to use.
        payload (bytes): The data to sign.

    Returns:
        bytes: The HMAC signature.

    Raises:
        ValueError: If the specified hash algorithm is not supported
                    or considered insecure.
    """
    # Normalize name for lookup
    algo = hash_algorithm_name.lower()

    if algo not in SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm_name}")

    # For SHAKE algorithms we need to specify a digest size (e.g., 32 bytes)
    if algo in ('shake_128', 'shake_256'):
        # Pick a default digest size (32 bytes) – adjust as needed
        digest_size = 32
        hmac_obj = hmac.new(secret_key, payload, hashlib.sha3_512 if algo == 'shake_256' else hashlib.sha3_256)
        return hmac_obj.digest()[:digest_size]

    # Create the HMAC object with the chosen hash function
    hmac_obj = hmac.new(secret_key, payload, getattr(hashlib, algo))
    return hmac_obj.digest()