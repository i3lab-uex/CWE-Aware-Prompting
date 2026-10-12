#!/usr/bin/env python3
"""
Utility to validate a configuration file against its cryptographic signature.

The module exposes a single function, `validate_config_file`, which:
1. Reads the configuration file.
2. Checks that the supplied signature matches the trusted signature
   stored in the global dictionary `TRUSTED_CONFIG_SIGNATURES`.
3. Returns the parsed configuration as a Python dictionary if the signature is
   valid, otherwise returns None.

The comparison uses :func:`hmac.compare_digest` to avoid timing‑attack
vulnerabilities (CWE‑347).
"""

from __future__ import annotations

import json
import hmac
import os
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Global dictionary mapping filenames to their trusted cryptographic signatures.
# In a real system this might be loaded from a secure source or environment
# variable. For illustration purposes it is defined statically here.
# --------------------------------------------------------------------------- #
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real filenames and signatures.
    "app_config.json": "a1b2c3d4e5f67890123456789abcdef0",
    "service_config.yaml": "0123456789abcdef0123456789abcdef",
}


def validate_config_file(filename: str, cryptographic_signature: str) -> Optional[Dict]:
    """
    Validate a configuration file against its expected cryptographic signature.

    Parameters
    ----------
    filename : str
        Path to the configuration file.
    cryptographic_signature : str
        The signature supplied alongside the configuration data.

    Returns
    -------
    Optional[Dict]
        Parsed configuration dictionary if signature is valid; otherwise ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist.")

    # Retrieve the trusted signature for this file, if any
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_signature is None:
        # If the file is not in our trust store, consider it invalid
        return None

    # Compare signatures using a timing‑attack resistant comparison
    if not hmac.compare_digest(
        cryptographic_signature.strip().lower(),
        expected_signature.strip().lower()
    ):
        # Signature mismatch
        return None

    # Read and parse the configuration file safely
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            # Support both JSON and YAML if needed; for now assume JSON
            config_data = json.load(fh)
    except Exception as exc:
        # Any error reading/parsing the file should be treated as a failure
        raise IOError(f"Failed to read configuration file '{filename}': {exc}") from exc

    # Basic type check: ensure the parsed data is a dictionary
    if not isinstance(config_data, dict):
        return None

    return config_data


# --------------------------------------------------------------------------- #
# Example usage (commented out; remove comments to run)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         cfg = validate_config_file("app_config.json", "a1b2c3d4e5f67890123456789abcdef0")
#         if cfg is not None:
#             print("Configuration validated:", cfg)
#         else:
#             print("Invalid signature or untrusted file.")
#     except IOError as e:
#         print(f"Error: {e}")