import hashlib
import hmac

# Supported hash algorithms (kept in sync with hashlib.algorithms_available)
SUPPORTED_ALGORITHMS = {
    "sha512", "sha256", "blake2s", "ripemd160",
    "sm3", "md5", "sha3_256", "sha512_224",
    "sha1", "sha384"
}


def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of `content` using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    content : bytes
        The message to authenticate.
    secret : bytes
        The key used for HMAC computation.

    Returns
    -------
    bytes
        The raw HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    # Normalise algorithm name to lower case for comparison
    algo_name = algorithm.lower()

    if algo_name not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Ensure the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm}' is not available on this system")

    # Create the HMAC object using the chosen hash function
    hmac_obj = hmac.new(secret, content, digestmod=hashlib.new(algo_name))
    return hmac_obj.digest()