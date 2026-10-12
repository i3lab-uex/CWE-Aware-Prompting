import json
import os

# Example trusted signatures dictionary.
# In a real application this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES = {
    "config.json": "abcd1234efgh5678",
    # add more filenames and their expected signatures here
}

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from `filename` and verify that its
    cryptographic signature matches the trusted value.

    Parameters
    ----------
    filename : str
        Name of the configuration file to load.
    cryptographic_signature : str
        Signature that accompanies the file.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If `filename` does not exist.
    """
    # Check that the file exists; raise IOError if it doesn't
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Retrieve the trusted signature for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # No trusted signature known for this file; treat as invalid
        return None

    # Compare signatures securely (constant‑time comparison)
    if not _secure_compare(expected_sig, cryptographic_signature):
        return None

    # Load and parse the configuration file
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Any error reading or parsing the file results in a failure
        return None

    if not isinstance(data, dict):
        # Configuration must be a dictionary; otherwise it's invalid
        return None

    return data


def _secure_compare(a: str, b: str) -> bool:
    """
    Constant‑time comparison of two strings to avoid timing attacks.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0