import os
import hmac

# Global dictionary of allowed file signatures (hexadecimal strings)
VALID_SIGNATURES = {
    # Example entries:
    # 'example.txt': '5f4dcc3b5aa765d61d8327deb882cf99',
    # Add actual signatures here
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Path to the file to be loaded.
    signature : str
        Hexadecimal string representing the expected cryptographic signature.

    Returns
    -------
    int
        1 if the file's signature is valid, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Retrieve the expected signature from the global dictionary
    expected_sig = VALID_SIGNATURES.get(file_name)
    if expected_sig is None:
        # No signature registered for this file – treat as invalid
        return 0

    # Normalize signatures to lowercase hex strings for comparison
    provided_sig = signature.lower()
    expected_sig = expected_sig.lower()

    # Use constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(provided_sig, expected_sig):
        # Here you would normally load/process the file
        return 1

    return 0