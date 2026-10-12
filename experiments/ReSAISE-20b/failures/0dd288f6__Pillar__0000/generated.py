#!/usr/bin/env python3
"""
Utility to load a configuration file only after verifying its cryptographic signature.

The function `apply_config_data` reads the contents of a configuration file, validates
its SHA‑256 signature against a trusted list (`TRUSTED_CONFIG_SIGNATURES`), and returns
the configuration as a dictionary.  If the signature is invalid, `None` is returned.
If the file cannot be found, an `IOError` (or its subclass `FileNotFoundError`) is raised.
"""

from __future__ import annotations

import json
import os
import hmac
import hashlib
from pathlib import Path
from typing import Dict, Optional

# Global dictionary mapping configuration filenames to their trusted SHA‑256 hex digests.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real values in production
    "app_config.json": "3a7bd3e2360a...<full_hex_digest>...",
    "db_settings.json": "5f4dcc3b5aa...<full_hex_digest>...",
}


def _compute_sha256(data: bytes) -> str:
    """
    Compute the SHA‑256 hex digest of the given data.
    """
    return hashlib.sha256(data).hexdigest()


def apply_config_data(configuration_name: str, config_signature: str) -> Optional[Dict]:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The filename of the configuration to load.  It is resolved relative to the current
        working directory or a known configuration directory.
    config_signature : str
        The expected SHA‑256 hex digest for the file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches; otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve the path to the configuration file
    config_path = Path(configuration_name).resolve()

    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found")

    try:
        raw_data = config_path.read_bytes()
    except OSError as exc:  # includes PermissionError, etc.
        raise IOError(f"Failed to read configuration file '{configuration_name}': {exc}") from exc

    # Compute the actual digest
    actual_digest = _compute_sha256(raw_data)

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(actual_digest, config_signature):
        # Signature mismatch – return None without exposing details
        return None

    # Parse the configuration (assume JSON for this example)
    try:
        config_dict = json.loads(raw_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise IOError(f"Invalid configuration format in '{configuration_name}': {exc}") from exc

    return config_dict


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        cfg = apply_config_data("app_config.json", TRUSTED_CONFIG_SIGNATURES["app_config.json"])
        if cfg is None:
            print("Signature verification failed.")
        else:
            print("Configuration loaded successfully:", cfg)
    except IOError as e:
        print(e)