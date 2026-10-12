import hashlib
import hmac

# List of cryptographically secure hash algorithms that are safe for HMAC usage.
SECURE_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha512_256',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
    # SHAKE algorithms are not deterministic in length, so they are excluded.
}

# The secret key used for HMAC signing. In practice this should be stored securely
# (e.g., in a key management service). For demonstration purposes we hard‑code it.
SECRET_KEY = b'super_secret_key'

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using a secure hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        Raw data that needs to be signed.

    Returns
    -------
    bytes
        The generated HMAC signature.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name to lowercase
    algo = algorithm.lower()

    # Check that the algorithm is both available in hashlib and marked secure
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure algorithm: {algorithm}")

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm not available: {algorithm}")

    # Create the HMAC object with the chosen digest
    hmac_obj = hmac.new(SECRET_KEY, message, digestmod=algo)
    return hmac_obj.digest()