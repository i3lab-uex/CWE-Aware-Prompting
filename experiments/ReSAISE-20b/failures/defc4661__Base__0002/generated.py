#!/usr/bin/env python3
"""
Utility to load a configuration file after verifying its cryptographic signature.
"""

import json
import os
from typing import Dict, Optional

# Global mapping of filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries; in real use these would be actual secure signatures.
    "app_config.json": "abcd1234efgh5678ijkl9012mnop3456",
    # Add more trusted signatures here.
}

def handle_config_file(file_name: str, sign: str) -> Optional[Dict]:
    """
    Load a configuration file after verifying its signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to load.
    sign : str
        Cryptographic signature supplied for verification.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid;
        otherwise, returns None.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path to avoid directory traversal attacks
    base_dir = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, file_name)

    # Verify that the file exists
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{file_name}' not found at {config_path}")

    # Verify the provided signature against the trusted value
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sig is None:
        # No trusted signature for this file; treat as untrusted
        return None

    # Use a constant-time comparison to avoid timing attacks
    from hmac import compare_digest
    if not compare_digest(sign, expected_sig):
        # Signature mismatch: do not load the file
        return None

    # Read and parse the configuration file safely
    try:
        with open(config_path, "r", encoding="utf-8") as fp:
            content = fp.read()
        config_data = json.loads(content)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to read or parse configuration file '{file_name}': {exc}") from exc

    # Ensure the result is a dictionary
    if not isinstance(config_data, dict):
        raise IOError(f"Configuration file '{file_name}' does not contain a JSON object")

    return config_data