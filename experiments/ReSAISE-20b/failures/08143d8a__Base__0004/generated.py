#!/usr/bin/env python3
"""
Utility for securely evaluating configuration files with cryptographic signatures.
"""

import json
import os
import hmac

# Global mapping of trusted signatures to file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real signatures in production
    "f5a3b9c1d2e4f6...": "config_a.json",
    "a1b2c3d4e5f6g7...": "config_b.json",
}

def evaluate_config_file(config_filename: str, provided_sig: str) -> dict | None:
    """
    Read and validate a configuration file against its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        The name of the configuration file to load.
    provided_sig : str
        The cryptographic signature supplied with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' not found")

    # Retrieve the expected signature for this file
    expected_sig = None
    for sig, fname in TRUSTED_CONFIG_SIGNATURES.items():
        if os.path.abspath(fname) == os.path.abspath(config_filename):
            expected_sig = sig
            break

    if expected_sig is None:
        # No trusted signature for this file – treat as invalid
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE-347)
    if not hmac.compare_digest(provided_sig, expected_sig):
        return None

    # Load the configuration data
    try:
        with open(config_filename, "r", encoding="utf-8") as fh:
            config_data = json.load(fh)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{config_filename}': {exc}") from exc

    # Basic sanity check: ensure it's a dictionary
    if not isinstance(config_data, dict):
        return None

    return config_data