import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of the given message using the specified hash algorithm and secret key.

    Args:
        algo (str): The name of the hash algorithm to use.
        msg (bytes): The message to authenticate.
        secret_key (bytes): The HMAC key.

    Returns:
        bytes: The computed HMAC digest.

    Raises:
        ValueError: If the requested algorithm is not supported.
    """
    # Normalize algorithm name to lower case for comparison
    algo_normalized = algo.lower()

    # Check if the algorithm is available in this Python build
    if algo_normalized not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Create a new HMAC object using the selected digest
    try:
        hmac_obj = hmac.new(secret_key, msg=msg, digestmod=algo_normalized)
    except Exception as exc:
        # In case the algorithm name is accepted by hmac but fails internally
        raise ValueError(f"Failed to create HMAC with algorithm {algo}: {exc}") from exc

    # Return the raw bytes of the digest
    return hmac_obj.digest()