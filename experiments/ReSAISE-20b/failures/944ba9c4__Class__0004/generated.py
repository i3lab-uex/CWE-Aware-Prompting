#!/usr/bin/env python3
"""
validate_config_file module

This module provides a single function `validate_config_file` that reads a
configuration file, verifies its cryptographic signature against a trusted
signature list, and returns the configuration data as a dictionary.

Security notes:
- The signature comparison uses `hmac.compare_digest` to prevent timing
  attacks.
- JSON is used for the configuration format; if the file contains invalid
  JSON, a `json.JSONDecodeError` will be raised.
- If the requested file does not exist, an `IOError` is raised.

"""

import json
import os
import hmac

# Global dictionary mapping filenames to their trusted signatures.
# In a real application this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx",
    "db_config.json":  "1234abcd5678efgh9012ijkl3456mnop7890qrst",
    # Add more trusted signatures here
}


def validate_config_file(filename: str, cryptographic_signature: str) -> dict | None:
    """
    Retrieve configuration data from `filename` and verify its cryptographic
    signature against the trusted list.

    Parameters:
        filename (str): Name of the configuration file to read.
        cryptographic_signature (str): Signature provided alongside the config.

    Returns:
        dict: Parsed configuration data if signature is valid.
        None: If the signature does not match any trusted signature.

    Raises:
        IOError: If `filename` does not exist or cannot be opened.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Read the entire file content
    with open(filename, "rb") as f:
        raw_data = f.read()

    # Verify the signature
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if not trusted_sig:
        # No trusted signature for this file – treat as invalid
        return None

    # Use constant-time comparison to avoid timing attacks
    if not hmac.compare_digest(cryptographic_signature, trusted_sig):
        return None

    # Parse JSON configuration
    try:
        config = json.loads(raw_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        # If the file contents are not valid JSON, raise an error
        raise ValueError(f"Invalid configuration format in '{filename}': {e}")

    return config