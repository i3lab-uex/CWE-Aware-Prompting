import os
import hmac

# Global dictionary of allowed file signatures.
# Example: {"example.txt": "abc123...", ...}
VALID_SIGNATURES = {
    # Populate with actual signatures in production
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source only if its cryptographic
    signature is present in the VALID_SIGNATURES dictionary.

    Parameters
    ----------
    file_name : str
        Path to the file that should be loaded.
    signature : str
        Cryptographic signature of the file.

    Returns
    -------
    int
        1 if the signature is valid, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the specified path.
    """
    # Verify that the file exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Fetch the expected signature for this file, if any
    expected_sig = VALID_SIGNATURES.get(file_name)

    # If the file is not in the whitelist, treat it as invalid
    if expected_sig is None:
        return 0

    # Use constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(signature, expected_sig):
        return 1

    return 0