import hashlib
import hmac

# Global secret key used for signing (should be set securely by the caller)
secret_key: bytes = b''  # placeholder, replace with a real key in production


def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    data : bytes
        The payload to sign.

    Returns
    -------
    bytes
        HMAC digest of the data using the chosen hash algorithm.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Normalise the hash name (hashlib uses lower‑case names)
    algo = hash_name.lower()

    # Verify that the algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create the hash object
    try:
        hash_obj = hashlib.new(algo)
    except (TypeError, ValueError) as exc:
        # Some algorithms may require additional arguments; fail explicitly
        raise ValueError(f"Failed to initialise hash '{hash_name}': {exc}") from exc

    # Compute HMAC
    signature = hmac.new(secret_key, data, hash_obj).digest()
    return signature