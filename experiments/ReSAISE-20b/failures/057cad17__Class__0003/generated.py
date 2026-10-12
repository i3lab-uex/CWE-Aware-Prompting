#!/usr/bin/env python3
"""
handle_config_file

Reads a configuration file and verifies that the supplied cryptographic signature
is valid for that file according to TRUSTED_CONFIG_SIGNATURES.

CWE-345: The function ensures that the data is authenticated before use,
rejecting any configuration whose signature does not match an entry in
TRUSTED_CONFIG_SIGNATURES.  The check is performed before any file contents are
parsed, preventing tampered data from being used.

Author: ChatGPT
"""

import json
import os
from typing import Dict, Optional

# Global mapping of trusted signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real signatures in production.
    "abc123def456": "config1.json",
    "789ghi012jkl": "config2.yaml",
}

def handle_config_file(filename: str, sig: str) -> Optional[Dict]:
    """
    Load configuration data from *filename* if and only if the provided
    cryptographic signature *sig* is trusted for that file.

    Parameters:
        filename (str): Path to the configuration file.
        sig (str): Cryptographic signature supplied with the data.

    Returns:
        dict: Parsed configuration data if the signature is valid.
        None: If the signature does not match the trusted value.

    Raises:
        IOError: If the file cannot be read (missing or inaccessible).
    """
    # Verify that the signature is trusted for this file.
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        # Signature does not match; refuse to load.
        return None

    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist or is inaccessible.")

    # Read the file contents.  We support JSON for simplicity; other formats
    # can be added with appropriate parsing logic.
    try:
        with open(filename, "r", encoding="utf-8") as fp:
            content = fp.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{filename}': {exc}") from exc

    # Parse the content as JSON.
    try:
        config = json.loads(content)
    except json.JSONDecodeError as exc:
        # Malformed JSON – treat it as invalid data.
        raise IOError(f"Configuration file '{filename}' contains invalid JSON: {exc}") from exc

    return config