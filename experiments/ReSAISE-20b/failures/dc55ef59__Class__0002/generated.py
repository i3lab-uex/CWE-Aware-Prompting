import hmac
import hashlib

# --------------------------------------------------------------------
# NOTE: In a real application the secret key should be stored securely
# (e.g., in an environment variable, a secrets manager, or a key vault).
# Here we provide a placeholder value for demonstration purposes.
# --------------------------------------------------------------------
SECRET_KEY: bytes = b"YOUR_SECURE_SECRET_KEY"

# List of hash algorithms considered secure for HMAC usage.
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

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or disallowed.
    """
    # Normalise the algorithm name to lower case
    algo_name = algo_name.lower()

    # Validate that the algorithm is both available and secure
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is unsupported or disallowed.")

    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_name}' is not available on this platform.")

    # Create the HMAC object with the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, message, digestmod=algo_name)

    # Return the raw digest bytes
    return hmac_obj.digest()