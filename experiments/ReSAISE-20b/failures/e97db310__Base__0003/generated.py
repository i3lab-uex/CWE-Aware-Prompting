import os
import hmac

# Example of a global dictionary that contains the allowed cryptographic signatures.
# In a real-world scenario this would be populated from a secure source.
VALID_SIGNATURES = {
    # "filename": "hex_encoded_signature"
    "example.txt": "5f4dcc3b5aa765d61d8327deb882cf99",
    # Add more entries as needed.
}


def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from the filesystem after verifying its cryptographic signature.

    Args:
        file_name (str): The name of the file to be loaded.
        signature (str): The cryptographic signature provided for verification.

    Returns:
        int: 1 if the file signature is valid, otherwise 0.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    # Verify that the file exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Retrieve the expected signature from the global dictionary
    expected_signature = VALID_SIGNATURES.get(file_name)

    # If the file is not in the whitelist, treat it as invalid
    if expected_signature is None:
        return 0

    # Perform a constant-time comparison to avoid timing attacks
    if hmac.compare_digest(signature, expected_signature):
        return 1
    else:
        return 0