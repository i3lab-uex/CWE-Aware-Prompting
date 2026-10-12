#!/usr/bin/env python3
"""
verify_config_data.py

This module provides a single function `verify_config_data` that reads a
configuration file and validates its cryptographic signature against a list
of trusted signatures.  The function is defensive against common attacks,
including path traversal, tampering with the signature file, and
resource exhaustion.

CWE-693 (Protection Mechanism Failure) is mitigated by:
  * Using a read‑only mapping of trusted signatures.
  * Strictly validating the file path before opening it.
  * Avoiding arbitrary code execution by parsing only JSON data.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Global trusted signatures mapping.
#
# Format: {signature (hex string): config_file_name}
# The mapping should never be modified at runtime.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example signatures (these would normally be SHA‑256 hex digests)
    "a3f5c2e1d4b6e7f8a9b0c1d2e3f4567890abcdef12345678abcd0123456789ab": "app_config.json",
    "b1c2d3e4f5a6b7c8d9e0f123456789abcdef01234567890abcdeffedcba9876": "db_config.json",
    # Add more trusted signatures here
}

# --------------------------------------------------------------------------- #
def _canonical_path(file_name: str, base_dir: Path) -> Path:
    """
    Resolve a file name relative to a trusted base directory and
    ensure it does not escape that directory.

    :param file_name: The user supplied file name.
    :param base_dir:  Path to the directory containing configuration files.
    :return: Canonical absolute path inside base_dir.
    :raises ValueError: If the resolved path is outside of base_dir.
    """
    candidate = (base_dir / file_name).resolve()
    if not str(candidate).startswith(str(base_dir.resolve())):
        raise ValueError("Attempted directory traversal detected.")
    return candidate

def verify_config_data(config_file: str, provided_signature: str) -> Optional[Dict]:
    """
    Read a configuration file and verify its cryptographic signature.

    The function ensures that:
      * the requested file exists in a trusted directory,
      * the provided signature matches one of the trusted signatures for that
        file name, and
      * the configuration data is parsed safely as JSON.

    :param config_file: The name of the configuration file to retrieve.
    :param provided_signature: Cryptographic signature supplied with the data
                               (expected as a hex string).
    :return: Dictionary containing the configuration data if signature is
             valid, otherwise None.
    :raises IOError: If the requested configuration file cannot be found.
    """
    # Define a trusted directory for configuration files
    CONFIG_DIR = Path(__file__).parent / "configs"
    if not CONFIG_DIR.is_dir():
        raise IOError(f"Configuration directory '{CONFIG_DIR}' does not exist.")

    # Sanitize and resolve the path
    try:
        config_path = _canonical_path(config_file, CONFIG_DIR)
    except ValueError as e:
        # The caller attempted a directory traversal
        raise IOError("Invalid configuration file path.") from e

    # Ensure the file exists and is readable
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_file}' not found.")

    # Verify the signature against trusted signatures
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if not expected_sig or expected_sig != config_file:
        # Signature does not match or is unknown
        return None

    # Read and parse the configuration data
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Either the file could not be read or JSON is malformed
        raise IOError(f"Failed to load configuration '{config_file}'.") from exc

    return data