import hashlib
import hmac

# Define a set of algorithms considered insecure for this context.
INSECURE_ALGORITHMS = {
    "md5",
    "sha1",
    "sha224",  # considered weak for some contexts; adjust as needed
    "md5-sha1",
}

def create_checksum(algorithm_name: str, message_data: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the provided data using the
    specified hash algorithm.

    Parameters:
        algorithm_name (str): Name of the hashing algorithm to use.
        message_data (bytes): Raw data that needs to be signed.

    Returns:
        bytes: The generated HMAC signature.

    Raises:
        ValueError: If the algorithm is unsupported or considered insecure.
    """
    # Normalize algorithm name
    algo = algorithm_name.lower()

    # Verify that the algorithm exists in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Ensure the algorithm is not in the insecure set
    if algo in INSECURE_ALGORITHMS:
        raise ValueError(f"Insecure hash algorithm selected: {algorithm_name}")

    # Use a static secret key for demonstration purposes.
    # In production, this should be securely generated and stored.
    secret_key = b"my_very_secret_key"

    # Create HMAC using the selected algorithm
    hmac_obj = hmac.new(secret_key, message_data, digestmod=algo)
    return hmac_obj.digest()