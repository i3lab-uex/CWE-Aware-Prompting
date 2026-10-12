import os
import hmac

# Global dictionary mapping file names to their valid cryptographic signatures.
VALID_SIGNATURES = {
    # Example entries:
    # "example.txt": "a3f5c2e8d1b9...",
    # Add actual signatures here.
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after verifying its cryptographic signature.

    Args:
        file_name (str): The name of the file to be loaded.
        signature (str): The cryptographic signature claimed for the file.

    Returns:
        int: 1 if the signature is valid and the file exists, otherwise 0.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    # Ensure the file actually exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Retrieve the expected signature from the global dictionary
    expected_sig = VALID_SIGNATURES.get(file_name)

    # If there is no entry for this file, treat it as invalid
    if expected_sig is None:
        return 0

    # Perform a constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(signature, expected_sig):
        return 1

    # Signature mismatch
    return 0