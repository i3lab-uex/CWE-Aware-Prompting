import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given data using the specified hash algorithm.

    Args:
        hash_algo (str): Name of the hash function to use (e.g., 'sha256', 'blake2s').
        input_data (bytes): The data to sign.
        secret_key (bytes): The secret key for HMAC.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the requested hash algorithm is not supported by hashlib.
    """
    # Normalize algorithm name to lower case
    algo_name = hash_algo.lower()

    # Check if the requested algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

    # Create the HMAC object using the specified hash function
    hmac_obj = hmac.new(secret_key, input_data, digestmod=algo_name)

    # Return the raw bytes of the HMAC signature
    return hmac_obj.digest()