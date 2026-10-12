import os
import hmac

# Global dictionary mapping file names to their valid cryptographic signatures.
# Example: {"example.txt": "a1b2c3d4..."}
VALID_SIGNATURES = {
    # Populate with actual signatures in production
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name of the file to be loaded.
    signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    int
        1 if the file exists and its signature is valid, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    """
    # Check that the file exists before attempting to read it
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Retrieve the expected signature for this file from the global dictionary
    expected_sig = VALID_SIGNATURES.get(file_name)

    # If we have no entry for this file, treat it as invalid
    if expected_sig is None:
        return 0

    # Perform a constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(signature, expected_sig):
        return 1

    return 0