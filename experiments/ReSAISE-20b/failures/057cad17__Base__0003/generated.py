#!/usr/bin/env python3
"""
handle_config_file.py

Safely read a configuration file and verify its cryptographic signature.
"""

import json
import os
import hmac

# Global mapping of trusted signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; in practice these would be populated elsewhere.
    # "signature1": "config_a.json",
    # "signature2": "config_b.json",
}

def handle_config_file(filename: str, sig: str):
    """
    Read a configuration file and verify its signature.

    Parameters
    ----------
    filename : str
        The name of the configuration file to retrieve.
    sig : str
        The cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid;
        otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Verify that the provided signature is trusted for this file.
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        # Either the signature is unknown or it does not match this file.
        return None

    # Ensure the file exists and is readable.
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' is missing")

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:  # Catch JSON errors, IO errors, etc.
        raise IOError(f"Failed to read configuration file '{filename}': {e}")

    # Additional sanity checks can be performed here (schema validation, etc.)
    return config