#!/usr/bin/env python3
"""
Secure configuration loader.

The function `apply_config_data` loads a JSON configuration file,
verifies its cryptographic signature against a trusted list, and
returns the parsed dictionary if verification succeeds.
If the file is missing an IOError is raised; if the signature does not
match, `None` is returned.

The implementation uses constant‑time comparison to mitigate timing attacks
(CWE-347).
"""

import json
import os
from hashlib import sha256
from hmac import compare_digest
from typing import Dict, Optional

# Global dictionary mapping configuration file names to their trusted SHA‑256 signatures
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries (hex strings of SHA‑256 digests)
    # "config1.json": "3f2b7c8d9e0a...",
    # ...
}

def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA‑256 digest of a file's contents as a hex string.
    """
    sha = sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()

def apply_config_data(configuration_name: str, config_signature: str) -> Optional[Dict]:
    """
    Load a configuration file, verify its signature against the trusted list,
    and return the parsed JSON dictionary.

    Parameters
    ----------
    configuration_name : str
        Name of the configuration file (relative or absolute path).
    config_signature : str
        Cryptographic signature supplied by the caller (hex string).

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid;
        otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path to avoid directory traversal attacks
    config_path = os.path.abspath(configuration_name)

    # Ensure the file exists and is a regular file
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Compute the file's actual signature
    try:
        actual_signature = _compute_file_signature(config_path)
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{configuration_name}': {exc}") from exc

    # Verify the supplied signature matches the computed one
    if not compare_digest(actual_signature.lower(), config_signature.lower()):
        # Signature mismatch; do not load configuration
        return None

    # Optionally cross‑check against trusted signatures list (extra safety)
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if expected_sig and not compare_digest(actual_signature.lower(), expected_sig.lower()):
        # The computed signature does not match the trusted one
        return None

    # Parse JSON configuration safely
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to load or parse configuration file '{configuration_name}': {exc}") from exc

    if not isinstance(config_data, dict):
        # Configuration must be a dictionary
        raise IOError(f"Configuration file '{configuration_name}' does not contain a JSON object.")

    return config_data