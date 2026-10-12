import os

# Example dictionary of allowed file signatures (hashes, e.g. SHA256)
VALID_SIGNATURES = {
    # 'file_name': 'expected_signature',
    # e.g. 'example.txt': 'a3f5c2...'
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from disk only if its cryptographic signature matches the
    allowed signature in VALID_SIGNATURES. Raises FileNotFoundError if the file
    does not exist.

    Parameters:
        file_name (str): The name of the file to load.
        signature (str): The cryptographic signature supplied by the caller.

    Returns:
        int: 1 if the file's signature is valid, 0 otherwise.
    """
    # Ensure we are working with a clean relative path to avoid directory traversal
    safe_path = os.path.normpath(file_name)
    if os.path.isabs(safe_path) or safe_path.startswith(".."):
        raise ValueError("Invalid file path")

    if not os.path.isfile(safe_path):
        # The file does not exist
        raise FileNotFoundError(f"No such file: {safe_path}")

    # Check that the signature is known for this file
    expected_sig = VALID_SIGNATURES.get(safe_path)
    if expected_sig is None:
        # File not listed as allowed
        return 0

    # Compare the provided signature with the expected one in a constant‑time manner
    # to avoid timing attacks (CWE-693).
    if _constant_time_compare(signature, expected_sig):
        return 1
    else:
        return 0


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0