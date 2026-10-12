import os
import hmac

# Example global dictionary containing allowed signatures.
# In practice this would be populated with real cryptographic hashes
VALID_SIGNATURES = {
    "example.txt": "5d41402abc4b2a76b9719d911017c592",
    # add more file_name: signature pairs as needed
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from disk after validating its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name (path) of the file to be loaded.
    signature : str
        The cryptographic signature of the file, e.g. an MD5 or SHA256 hex digest.

    Returns
    -------
    int
        1 if the file signature is valid and the file was loaded successfully,
        0 otherwise.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist on disk.
    """
    # Check that the file exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Load the file (contents are not used beyond signature validation)
    with open(file_name, "rb") as f:
        _ = f.read()

    # Retrieve the expected signature for this file
    expected_sig = VALID_SIGNATURES.get(file_name)
    if expected_sig is None:
        # No signature known for this file – treat as invalid
        return 0

    # Use a constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(signature.lower(), expected_sig.lower()):
        return 1
    else:
        return 0