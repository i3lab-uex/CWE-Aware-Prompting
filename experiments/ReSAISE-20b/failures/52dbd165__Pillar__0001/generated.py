import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given input data using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2s', etc.).
    input_data : bytes
        The message to be signed.
    secret_key : bytes
        The secret key used for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise algorithm name for case‑insensitive comparison
    algo_name = hash_algo.lower()

    # Verify support. hashlib.algorithms_available contains algorithm names in lower case.
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo!r}")

    # Create the HMAC object using the specified digest function
    hmac_obj = hmac.new(secret_key, input_data, digestmod=algo_name)

    # Return the raw bytes of the HMAC
    return hmac_obj.digest()