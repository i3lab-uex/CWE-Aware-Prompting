import os
import hmac

# Global dictionary mapping file names to their allowed cryptographic signatures.
# Example: VALID_SIGNATURES = {"example.txt": "abc123...", ...}
VALID_SIGNATURES = {
    # Populate with actual file signatures as needed.
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from disk only if its cryptographic signature is valid.

    Args:
        file_name (str): The name of the file to load.
        signature (str): The cryptographic signature provided for validation.

    Returns:
        int: 1 if the file signature matches a known valid signature, otherwise 0.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    # Ensure the file exists; raise FileNotFoundError if it doesn't.
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"No such file: '{file_name}'")

    # Retrieve the expected signature for this file, if any.
    expected_sig = VALID_SIGNATURES.get(file_name)

    # If the file is not in the list of allowed signatures, consider it invalid.
    if expected_sig is None:
        return 0

    # Use a constant‑time comparison to avoid timing attacks.
    is_valid = hmac.compare_digest(signature.encode('utf-8'), expected_sig.encode('utf-8'))

    return 1 if is_valid else 0