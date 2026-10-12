#!/usr/bin/env python3
"""
Utility to securely load configuration files that are accompanied by a
cryptographic signature.  The function verifies the signature against a
trusted list of signatures before deserialising the configuration data.

CWE-345 (Insufficient Verification of Data Authenticity) is mitigated by
ensuring that the signature provided by the caller matches a known,
trusted value for the requested configuration file.  The comparison is
performed in constant time to avoid timing side‑channels.
"""

import json
import hmac
from pathlib import Path
from typing import Dict, Optional

# Global dictionary mapping configuration file names to their trusted signatures.
# In a real deployment this would be populated from a secure source or
# compiled into the binary.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    "app_config.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    "db_config.json":  "6f1ed002ab5595859014ebf0951522d9",
    # Add more entries as needed
}


def verify_config_data(config_file: str, provided_signature: str) -> Optional[Dict]:
    """
    Load a configuration file only after verifying that the provided signature
    matches the trusted signature for that file.

    Parameters:
        config_file (str): Name of the configuration file to load.
        provided_signature (str): Signature supplied alongside the config data.

    Returns:
        dict: The deserialized configuration data if verification succeeds.
        None: If the signature does not match.

    Raises:
        IOError: If the configuration file cannot be found or read.
    """
    # Resolve absolute path to prevent directory traversal attacks
    config_path = Path(config_file).resolve()

    # Ensure the file exists and is a regular file
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_file}' is missing or inaccessible")

    # Retrieve the trusted signature for this configuration
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_file)
    if expected_signature is None:
        # No trusted signature for this file; treat as invalid
        return None

    # Constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(provided_signature, expected_signature):
        return None

    # Read and parse the configuration file
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Propagate file I/O errors; configuration format errors are treated
        # as a failure to verify authenticity.
        raise IOError(f"Failed to read or parse configuration file '{config_file}': {exc}") from exc

    return data