import json
import os

# Global dictionary mapping filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries
    "app_config.json": "a1b2c3d4e5f6g7h8i9j0",
    "db_config.json": "0123456789abcdef1234",
}

def validate_config_file(filename: str, cryptographic_signature: str) -> dict | None:
    """
    Load configuration data from *filename* and verify that the provided
    cryptographic signature matches the trusted signature for this file.

    Parameters
    ----------
    filename : str
        Path to the configuration file.
    cryptographic_signature : str
        Signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        The parsed JSON configuration if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If *filename* does not exist or cannot be read.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist.")

    # Retrieve the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # No trusted signature known for this file – treat as invalid
        return None

    # Compare signatures in a timing‑attack resistant way
    if not _constant_time_compare(expected_sig, cryptographic_signature):
        return None

    # Read and parse the configuration file
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read or parse configuration file '{filename}': {exc}") from exc

    # Ensure the parsed data is a dictionary
    if not isinstance(data, dict):
        return None

    return data


def _constant_time_compare(a: str, b: str) -> bool:
    """
    Perform a constant‑time comparison of two strings to mitigate timing attacks.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode("utf-8"), b.encode("utf-8")):
        result |= x ^ y
    return result == 0