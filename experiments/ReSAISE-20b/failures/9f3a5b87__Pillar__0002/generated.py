#!/usr/bin/env python3
"""
Utility to safely load configuration files that are accompanied by a cryptographic signature.
The function verifies that the provided signature matches the trusted one stored in
TRUSTED_CONFIG_SIGNATURES before loading the configuration data.
"""

import json
import os
from secrets import compare_digest

# Global mapping of trusted filenames to their expected signatures.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    # Add more trusted files and their signatures here.
}

def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve and validate configuration data from a JSON file.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to load.
    file_signature : str
        Cryptographic signature provided alongside the file.

    Returns
    -------
    dict | None
        Parsed configuration data if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the specified file does not exist or cannot be opened.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Retrieve the expected signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sig is None:
        # No trusted signature known for this file – reject it
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑693)
    if not compare_digest(file_signature, expected_sig):
        # Signature mismatch – reject the file
        return None

    # Read and parse the JSON configuration safely
    try:
        with open(file_name, "r", encoding="utf-8") as fp:
            config_data = json.load(fp)
    except (OSError, json.JSONDecodeError) as exc:
        # Propagate I/O errors; JSON errors indicate malformed config
        raise IOError(f"Failed to read or parse '{file_name}': {exc}") from exc

    # Return the configuration dictionary
    return config_data