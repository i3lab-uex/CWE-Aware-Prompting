import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash function to use (e.g., 'sha256', 'md5').
    content : bytes
        The message to be signed.
    secret : bytes
        The secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or unavailable.
    """
    # Normalise algorithm name to lowercase
    algo = algorithm_name.lower()

    # Check that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Compute HMAC using the chosen digest function
    try:
        signature = hmac.new(secret, content, algo).digest()
    except Exception as exc:   # pragma: no cover
        # In practice this should not happen if the algorithm check passed,
        # but we guard against any unexpected errors.
        raise ValueError(f"Failed to compute HMAC: {exc}") from exc

    return signature