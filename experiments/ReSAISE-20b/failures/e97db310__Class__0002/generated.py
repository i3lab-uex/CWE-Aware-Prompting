import os
import hmac

# Global dictionary mapping file names to their expected cryptographic signatures.
# Example: {"example.txt": "5f4dcc3b5aa765d61d8327deb882cf99"}
VALID_SIGNATURES = {
    # Populate with real signatures in production.
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from disk after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name (or relative path) of the file to be loaded.
    signature : str
        Cryptographic signature supplied for verification.

    Returns
    -------
    int
        1 if the file exists and its signature matches an entry in VALID_SIGNATURES,
        0 otherwise.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the given path.
    """
    # Verify that the file exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Retrieve the expected signature for this file
    expected = VALID_SIGNATURES.get(file_name)
    if expected is None:
        # No known signature for this file; treat as invalid
        return 0

    # Perform a constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(signature, expected):
        return 1
    else:
        return 0