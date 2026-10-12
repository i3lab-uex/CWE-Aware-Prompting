#!/usr/bin/env python3
"""
Module providing secure configuration loading with signature verification.
"""

import os
import json
import hmac
from typing import Dict, Optional

# Global mapping of trusted signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be generated
    # using a secure key and stored securely.
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "config.json",
    # Add more trusted signatures here.
}

def evaluate_config_file(config_filename: str, provided_sig: str) -> Optional[Dict]:
    """
    Load and return configuration data from *config_filename* after verifying that
    the provided signature is trusted for this file.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    provided_sig : str
        Cryptographic signature supplied alongside the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid; otherwise,
        ``None``.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Ensure the signature is in the trusted list and matches the file name
    expected_filename = TRUSTED_CONFIG_SIGNATURES.get(provided_sig)
    if not expected_filename:
        # Signature is unknown
        return None

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_filename, config_filename):
        return None

    # Resolve the absolute path to avoid directory traversal
    abs_path = os.path.abspath(config_filename)

    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{config_filename}' not found.")

    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to read or parse configuration file: {exc}") from exc

    return config_data