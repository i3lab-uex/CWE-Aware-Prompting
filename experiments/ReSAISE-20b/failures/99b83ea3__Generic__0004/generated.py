import hashlib
import hmac

# A set of hash algorithms that are considered secure for HMAC usage.
_SECURE_ALGORITHMS = {
    "sha512_256",
    "sha384",
    "sha512",
    "sha256",
    "sha224",
    "blake2b",
    "blake2s",
    "sha3_512",
    "sha3_384",
    "sha3_256",
    "sha3_224",
}

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the message.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    if algorithm_name.lower() not in _SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Secret key for HMAC; in a real application this would be stored securely.
    secret_key = b"your-very-secret-key"

    # Create a new HMAC object using the chosen hash algorithm.
    hmac_obj = hmac.new(secret_key, msg=message, digestmod=getattr(hashlib, algorithm_name.lower()))
    return hmac_obj.digest()