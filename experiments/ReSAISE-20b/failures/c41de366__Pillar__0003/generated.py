#!/usr/bin/env python3
"""
Utility to securely retrieve configuration data from a file and verify its cryptographic signature.

The function `retrieve_config_data` performs the following steps:
1. Checks that the file exists and is readable.
2. Reads the file contents as UTF‑8 text.
3. Verifies that the provided `crypt_signature` matches the trusted signature
   stored in the global dictionary `TRUSTED_CONFIG_SIGNATURES`.
4. Parses the file contents as JSON and returns it as a Python dictionary.

Security considerations:
- Uses `hmac.compare_digest` for constant‑time comparison of signatures
  to mitigate timing attacks (CWE-693).
- Raises `IOError` if the file cannot be accessed, providing clear
  feedback to the caller.
- The trusted signatures dictionary should contain only known good values;
  it is assumed that these are maintained securely elsewhere.
"""

import json
import pathlib
import hmac

# Global dictionary mapping configuration filenames to their trusted signatures.
# Example:
# TRUSTED_CONFIG_SIGNATURES = {
#     "app_config.json": "a1b2c3d4e5f6g7h8i9j0...",
#     "db_config.json":  "0123456789abcdef1234..."
# }
TRUSTED_CONFIG_SIGNATURES = {
    # Populate with actual trusted signatures.
}

def retrieve_config_data(config_filename: str, crypt_signature: str) -> dict | None:
    """
    Retrieve configuration data from `config_filename` after verifying that
    the supplied cryptographic signature matches the trusted value.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    crypt_signature : str
        Cryptographic signature sent with the configuration data.

    Returns
    -------
    dict | None
        Parsed JSON configuration as a dictionary if the signature is valid.
        Returns None if the signature does not match.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Resolve absolute path for safety
    config_path = pathlib.Path(config_filename).resolve()

    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    # Read the file contents
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data_text = f.read()
    except Exception as exc:
        raise IOError(f"Failed to read configuration file '{config_filename}': {exc}") from exc

    # Retrieve the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None:
        # No trusted signature known for this file
        return None

    # Constant‑time comparison of signatures to prevent timing attacks
    if not hmac.compare_digest(crypt_signature, expected_sig):
        return None

    # Parse JSON data
    try:
        config_dict = json.loads(data_text)
    except json.JSONDecodeError as exc:
        # Invalid JSON – treat as an integrity failure
        return None

    if not isinstance(config_dict, dict):
        # Configuration should be a JSON object
        return None

    return config_dict