import os
import hmac

# Global dictionary of allowed file signatures.
# Keys are file names, values are expected cryptographic signature strings.
VALID_SIGNATURES = {
    # Example entries:
    # "example.txt": "5f4dcc3b5aa765d61d8327deb882cf99",
    # "data.bin":   "e3b0c44298fc1c149afbf4c8996fb924"
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after validating its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name of the file to be loaded.
    signature : str
        The cryptographic signature claimed for this file.

    Returns
    -------
    int
        1 if the provided signature matches an entry in VALID_SIGNATURES, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the file does not exist on disk.
    """
    # Ensure the file exists before attempting to load it
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Retrieve the expected signature for this file, if any
    expected = VALID_SIGNATURES.get(file_name)

    # If no signature is registered for this file, reject it
    if expected is None:
        return 0

    # Use constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(signature, expected):
        # The file is considered valid; load it (e.g., read its contents)
        # For demonstration, we simply open the file to ensure it can be accessed.
        with open(file_name, 'rb') as f:
            _ = f.read()  # Discard content; replace with actual processing if needed
        return 1

    # Signature mismatch
    return 0